"""
ContaBot — Setup Completo
Executa todos os scripts de setup em sequencia.
"""
import os
import sys
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)


def run_script(name, args=None):
    """Executa um script Python e retorna se teve sucesso."""
    script_path = os.path.join(SCRIPTS_DIR, name)
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    print(f"\n{'='*60}")
    print(f"Executando: {name}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, cwd=ROOT_DIR)
    return result.returncode == 0


def check_env():
    """Verifica se o .env esta configurado."""
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT_DIR, ".env"))

    required = [
        "UAZAPI_TOKEN",
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        "ANTROPIC_API_KEY",
        "ESCRITORIO_NOME",
        "CONTADOR_WHATSAPP",
    ]

    # Mais flexivel: checa as variaveis mais criticas
    critical = ["GOOGLE_SERVICE_ACCOUNT_FILE"]
    missing = []
    for var in critical:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print("ERRO: Variaveis de ambiente obrigatorias nao configuradas:")
        for var in missing:
            print(f"  - {var}")
        print("\nCopie .env.example para .env e preencha os valores.")
        return False

    sa_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
    if sa_file and not os.path.exists(os.path.join(ROOT_DIR, sa_file)):
        print(f"ERRO: Arquivo de Service Account nao encontrado: {sa_file}")
        print("Baixe o JSON da Service Account do Google Cloud Console.")
        return False

    return True


def main():
    print("""
   ____            _        ____        _
  / ___|___  _ __ | |_ __ _| __ )  ___ | |_
 | |   / _ \| '_ \| __/ _` |  _ \ / _ \| __|
 | |__| (_) | | | | || (_| | |_) | (_) | |_
  \____\___/|_| |_|\__\__,_|____/ \___/ \__|

  Setup Completo
    """)

    # Checa pre-requisitos
    print("Verificando pre-requisitos...")
    if not check_env():
        sys.exit(1)
    print("Pre-requisitos OK!\n")

    # Pergunta o que executar
    print("O que deseja configurar?")
    print("  1. Tudo (Sheets + Drive + Webhook)")
    print("  2. Apenas Google Sheets")
    print("  3. Apenas Google Drive")
    print("  4. Apenas Webhook UazAPI")
    print("  5. Importar clientes de CSV")

    choice = input("\nEscolha (1-5): ").strip()

    if choice == "1":
        run_script("setup_sheets.py")
        run_script("setup_drive.py")
        run_script("setup_webhook.py")

        csv_input = input("\nDeseja importar clientes de um CSV? (s/n): ").strip().lower()
        if csv_input == "s":
            csv_path = input("Caminho do CSV: ").strip()
            if os.path.exists(csv_path):
                run_script("import_clientes.py", [csv_path])
            else:
                print(f"Arquivo nao encontrado: {csv_path}")

    elif choice == "2":
        run_script("setup_sheets.py")

    elif choice == "3":
        csv_path = None
        csv_input = input("Tem CSV de clientes para criar pastas? (s/n): ").strip().lower()
        if csv_input == "s":
            csv_path = input("Caminho do CSV: ").strip()
        run_script("setup_drive.py", [csv_path] if csv_path else None)

    elif choice == "4":
        run_script("setup_webhook.py")

    elif choice == "5":
        csv_path = input("Caminho do CSV: ").strip()
        if os.path.exists(csv_path):
            run_script("import_clientes.py", [csv_path])
        else:
            print(f"Arquivo nao encontrado: {csv_path}")

    else:
        print("Opcao invalida.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("Setup finalizado!")
    print(f"{'='*60}")
    print("\nProximos passos:")
    print("  1. Importe os workflows JSON no n8n (pasta workflows/)")
    print("  2. Configure as credenciais Google no n8n")
    print("  3. Ative os workflows")
    print("  4. Teste enviando uma foto de documento no WhatsApp")


if __name__ == "__main__":
    main()
