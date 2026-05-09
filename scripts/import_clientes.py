"""
ContaBot — Importar Clientes
Le um CSV de clientes e popula a aba CLIENTES da planilha + cria pastas no Drive.
"""
import os
import sys
import csv
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import gspread
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SA_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "./credentials/service-account.json")
SHEETS_ID = os.getenv("CONTABOT_SHEETS_ID", "")
DRIVE_FOLDER_ID = os.getenv("CONTABOT_DRIVE_FOLDER_ID", "")


def get_credentials():
    return Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)


def create_folder(service, name, parent_id):
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(body=metadata, fields="id, webViewLink").execute()
    return folder["id"], folder.get("webViewLink", "")


def find_clientes_folder(service, root_id):
    """Encontra a pasta CLIENTES dentro da raiz."""
    q = f"'{root_id}' in parents and name='CLIENTES' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=q, fields="files(id)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    # Cria se nao existe
    fid, _ = create_folder(service, "CLIENTES", root_id)
    return fid


def main():
    if len(sys.argv) < 2:
        print("Uso: python import_clientes.py clientes.csv")
        print("\nFormato do CSV (com header):")
        print("  nome,cpf_cnpj,whatsapp,email,tipo")
        print('  Joao Silva,123.456.789-00,11999999999,joao@email.com,PF')
        print('  Empresa ABC,12.345.678/0001-99,11888888888,contato@abc.com,PJ Simples')
        sys.exit(1)

    csv_path = sys.argv[1]

    if not SHEETS_ID:
        print("ERRO: CONTABOT_SHEETS_ID nao configurado no .env")
        sys.exit(1)
    if not DRIVE_FOLDER_ID:
        print("ERRO: CONTABOT_DRIVE_FOLDER_ID nao configurado no .env")
        sys.exit(1)

    print(f"\n=== ContaBot — Importar Clientes ===")
    print(f"CSV: {csv_path}")
    print(f"Sheets ID: {SHEETS_ID}")
    print(f"Drive Folder: {DRIVE_FOLDER_ID}\n")

    creds = get_credentials()
    drive = build("drive", "v3", credentials=creds)
    gc = gspread.authorize(creds)

    sh = gc.open_by_key(SHEETS_ID)
    ws = sh.worksheet("CLIENTES")

    # Encontra pasta CLIENTES no Drive
    clientes_folder = find_clientes_folder(drive, DRIVE_FOLDER_ID)

    # Le clientes existentes pra evitar duplicatas
    existing = ws.col_values(3)  # Coluna C = CPF/CNPJ
    existing_set = set(existing[1:])  # Pula header

    # Le CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows_to_add = []
        count = 0
        skipped = 0

        for row in reader:
            nome = row.get("nome", row.get("Nome", "")).strip()
            doc = row.get("cpf_cnpj", row.get("CPF/CNPJ", row.get("documento", ""))).strip()
            whatsapp = row.get("whatsapp", row.get("WhatsApp", "")).strip().replace("+", "").replace("-", "").replace(" ", "")
            email = row.get("email", row.get("Email", "")).strip()
            tipo = row.get("tipo", row.get("Tipo", "PF")).strip()

            if not nome or not doc:
                print(f"  SKIP (dados incompletos): {row}")
                skipped += 1
                continue

            if doc in existing_set:
                print(f"  SKIP (ja existe): {doc} — {nome}")
                skipped += 1
                continue

            # Cria pasta no Drive
            folder_name = f"{doc} — {nome}"
            folder_id, folder_link = create_folder(drive, folder_name, clientes_folder)

            # Gera ID
            count += 1
            cli_id = f"CLI-{count:04d}"

            rows_to_add.append([
                cli_id,
                nome,
                doc,
                whatsapp,
                email,
                tipo,
                "Ativo",
                folder_link,
                datetime.now().strftime("%d/%m/%Y"),
                "",
            ])

            print(f"  + {cli_id} | {doc} — {nome} ({tipo})")
            existing_set.add(doc)

    # Append na planilha
    if rows_to_add:
        ws.append_rows(rows_to_add, value_input_option="USER_ENTERED")
        print(f"\n{len(rows_to_add)} clientes importados com sucesso!")
    else:
        print("\nNenhum cliente novo para importar.")

    if skipped:
        print(f"{skipped} clientes ignorados (duplicados ou incompletos)")


if __name__ == "__main__":
    main()
