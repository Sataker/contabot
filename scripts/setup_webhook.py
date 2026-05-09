"""
ContaBot — Setup Webhook UazAPI
Configura o webhook do UazAPI para apontar para o n8n.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("UAZAPI_BASE_URL", "https://spark.uazapi.com")
TOKEN = os.getenv("UAZAPI_TOKEN", "")
N8N_BASE = os.getenv("N8N_WEBHOOK_BASE", "")


def set_webhook(webhook_url):
    """Configura o webhook no UazAPI."""
    headers = {
        "token": TOKEN,
        "Content-Type": "application/json",
    }

    # Tenta v2 (uazapiGO)
    payload = {"webhookUrl": webhook_url}

    resp = requests.post(f"{BASE_URL}/webhook/set", json=payload, headers=headers)

    if resp.status_code == 200:
        print(f"Webhook configurado: {webhook_url}")
        print(f"Resposta: {resp.json()}")
        return True

    # Tenta endpoint alternativo
    resp = requests.put(f"{BASE_URL}/instance/webhook", json={"url": webhook_url}, headers=headers)

    if resp.status_code == 200:
        print(f"Webhook configurado (v2): {webhook_url}")
        return True

    print(f"Erro ao configurar webhook: {resp.status_code}")
    print(f"Resposta: {resp.text}")
    return False


def check_status():
    """Verifica status da conexao UazAPI."""
    headers = {"token": TOKEN}
    resp = requests.get(f"{BASE_URL}/session/status", headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        print(f"Status da sessao: {data}")
        return data

    print(f"Erro ao verificar status: {resp.status_code}")
    return None


def test_send(phone, message="Teste do ContaBot - se recebeu esta mensagem, o sistema esta funcionando!"):
    """Envia mensagem de teste."""
    headers = {
        "token": TOKEN,
        "Content-Type": "application/json",
    }
    payload = {
        "phone": phone,
        "message": message,
    }

    resp = requests.post(f"{BASE_URL}/message/text", json=payload, headers=headers)

    if resp.status_code == 200:
        print(f"Mensagem de teste enviada para {phone}")
        return True

    print(f"Erro ao enviar teste: {resp.status_code} — {resp.text}")
    return False


def main():
    print(f"\n=== ContaBot — Setup Webhook UazAPI ===\n")
    print(f"Base URL: {BASE_URL}")
    print(f"Token: {TOKEN[:8]}...{TOKEN[-4:]}" if len(TOKEN) > 12 else f"Token: {TOKEN}")

    if not TOKEN:
        print("\nERRO: UAZAPI_TOKEN nao configurado no .env")
        return

    # 1. Verifica status
    print("\n1. Verificando status da conexao...")
    check_status()

    # 2. Configura webhook
    if N8N_BASE:
        print("\n2. Configurando webhook...")
        # O webhook do n8n vai receber TODAS as mensagens
        # Os workflows filtram por tipo (imagem, texto, etc)
        webhook_url = f"{N8N_BASE}/contabot-intake"
        set_webhook(webhook_url)
    else:
        print("\n2. N8N_WEBHOOK_BASE nao configurado — pule esta etapa ou configure no .env")

    # 3. Teste de envio
    contador_wa = os.getenv("CONTADOR_WHATSAPP", "")
    if contador_wa:
        print("\n3. Enviando mensagem de teste...")
        test_send(contador_wa)
    else:
        print("\n3. CONTADOR_WHATSAPP nao configurado — teste manual necessario")

    print("\nSetup concluido!")


if __name__ == "__main__":
    main()
