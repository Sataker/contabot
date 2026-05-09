"""
ContaBot — Setup Google Drive
Cria a estrutura de pastas para o escritorio e opcionalmente para cada cliente.
"""
import os
import csv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive"]
SA_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "./credentials/service-account.json")
ESCRITORIO = os.getenv("ESCRITORIO_NOME", "Contabilidade XYZ")


def get_drive_service():
    creds = Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def create_folder(service, name, parent_id=None):
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = service.files().create(body=metadata, fields="id, webViewLink").execute()
    return folder["id"], folder.get("webViewLink", "")


def setup_estrutura_base(service):
    """Cria a pasta raiz e subpastas do escritorio."""
    print(f"Criando estrutura para: {ESCRITORIO}")

    root_id, root_link = create_folder(service, f"ContaBot — {ESCRITORIO}")
    print(f"  Pasta raiz: {root_link}")

    clientes_id, _ = create_folder(service, "CLIENTES", root_id)
    print(f"  /CLIENTES criada")

    modelos_id, _ = create_folder(service, "_MODELOS", root_id)
    print(f"  /_MODELOS criada")

    return root_id, clientes_id


def setup_cliente(service, clientes_folder_id, nome, documento, tipo="PF", ano=2026):
    """Cria a estrutura de pastas para um cliente individual."""
    folder_name = f"{documento} — {nome}"
    cliente_id, cliente_link = create_folder(service, folder_name, clientes_folder_id)
    print(f"  Cliente: {folder_name}")

    # Pasta do ano
    ano_id, _ = create_folder(service, str(ano), cliente_id)

    if tipo == "PF":
        # IRPF
        irpf_id, _ = create_folder(service, "IRPF", ano_id)
        create_folder(service, "informes", irpf_id)
        create_folder(service, "notas-medicas", irpf_id)
        create_folder(service, "educacao", irpf_id)
        create_folder(service, "outros", irpf_id)
        print(f"    /IRPF com subpastas")

    # MENSAIS (PF e PJ)
    mensais_id, _ = create_folder(service, "MENSAIS", ano_id)
    meses = [
        "01-JAN", "02-FEV", "03-MAR", "04-ABR", "05-MAI", "06-JUN",
        "07-JUL", "08-AGO", "09-SET", "10-OUT", "11-NOV", "12-DEZ"
    ]
    for mes in meses:
        mes_id, _ = create_folder(service, mes, mensais_id)
        if tipo != "PF":
            create_folder(service, "notas-fiscais", mes_id)
        create_folder(service, "guias", mes_id)
        create_folder(service, "extratos", mes_id)
        create_folder(service, "comprovantes", mes_id)
    print(f"    /MENSAIS com 12 meses")

    return cliente_id, cliente_link


def setup_clientes_csv(service, clientes_folder_id, csv_path):
    """Importa clientes de um CSV e cria pastas para cada um."""
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        resultados = []
        for row in reader:
            nome = row.get("nome", row.get("Nome", ""))
            documento = row.get("cpf_cnpj", row.get("CPF/CNPJ", row.get("documento", "")))
            tipo = row.get("tipo", row.get("Tipo", "PF"))

            if not nome or not documento:
                print(f"  SKIP: dados incompletos — {row}")
                continue

            cid, clink = setup_cliente(service, clientes_folder_id, nome, documento, tipo)
            resultados.append({
                "nome": nome,
                "documento": documento,
                "tipo": tipo,
                "folder_id": cid,
                "folder_link": clink,
            })
        return resultados


def main():
    import sys

    print(f"\n=== ContaBot — Setup Google Drive ===\n")

    service = get_drive_service()
    root_id, clientes_id = setup_estrutura_base(service)

    print(f"\nPasta raiz ID: {root_id}")
    print(f"Adicione no .env: CONTABOT_DRIVE_FOLDER_ID={root_id}")

    # Se passou um CSV como argumento, importa clientes
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        print(f"\nImportando clientes de: {csv_path}")
        resultados = setup_clientes_csv(service, clientes_id, csv_path)
        print(f"\n{len(resultados)} clientes criados no Drive")
        for r in resultados:
            print(f"  {r['documento']} — {r['nome']} → {r['folder_link']}")
    else:
        print("\nDica: passe um CSV para criar pastas dos clientes automaticamente:")
        print("  python setup_drive.py clientes.csv")
        print("\nFormato do CSV:")
        print("  nome,cpf_cnpj,tipo")
        print('  Joao Silva,123.456.789-00,PF')
        print('  Empresa ABC,12.345.678/0001-99,PJ Simples')


if __name__ == "__main__":
    main()
