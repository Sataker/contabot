"""
ContaBot — Teste Local de Webhook
Simula o payload que o UazAPI envia pro n8n, pra testar sem precisar enviar mensagem real.
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

N8N_BASE = os.getenv("N8N_WEBHOOK_BASE", "http://localhost:5678/webhook")


def simulate_text_message(phone="5511999999999", message="Que documentos preciso pro IR?"):
    """Simula mensagem de texto recebida."""
    payload = {
        "instance": "contabot-test",
        "event": "message",
        "data": {
            "id": "TEST_MSG_001",
            "from": f"{phone}@s.whatsapp.net",
            "body": message,
            "type": "text",
            "timestamp": 1715000000,
            "media": None,
        }
    }
    return payload


def simulate_image_message(phone="5511999999999", image_url="https://example.com/nota.jpg"):
    """Simula envio de imagem."""
    payload = {
        "instance": "contabot-test",
        "event": "message",
        "data": {
            "id": "TEST_MSG_002",
            "from": f"{phone}@s.whatsapp.net",
            "body": "",
            "type": "image",
            "timestamp": 1715000000,
            "media": {
                "url": image_url,
                "mimetype": "image/jpeg",
            },
        }
    }
    return payload


def simulate_document_message(phone="5511999999999", doc_url="https://example.com/guia.pdf"):
    """Simula envio de documento PDF."""
    payload = {
        "instance": "contabot-test",
        "event": "message",
        "data": {
            "id": "TEST_MSG_003",
            "from": f"{phone}@s.whatsapp.net",
            "body": "",
            "type": "document",
            "timestamp": 1715000000,
            "media": {
                "url": doc_url,
                "mimetype": "application/pdf",
                "filename": "guia_das.pdf",
            },
        }
    }
    return payload


def simulate_cadastro(phone="5511999988887"):
    """Simula mensagem de cadastro do contador."""
    payload = {
        "instance": "contabot-test",
        "event": "message",
        "data": {
            "id": "TEST_MSG_004",
            "from": f"{phone}@s.whatsapp.net",
            "body": "NOVO_CLIENTE\nNome: Maria Teste\nCPF: 999.888.777-66\nWhatsApp: 11977776666\nTipo: PF\nEmail: maria@teste.com",
            "type": "text",
            "timestamp": 1715000000,
            "media": None,
        }
    }
    return payload


def send_to_webhook(endpoint, payload):
    """Envia payload para o webhook do n8n."""
    url = f"{N8N_BASE}/{endpoint}"
    print(f"\nEnviando para: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")

    try:
        resp = requests.post(url, json=payload, timeout=30)
        print(f"Status: {resp.status_code}")
        print(f"Resposta: {resp.text[:500]}")
        return resp
    except requests.exceptions.ConnectionError:
        print(f"ERRO: Nao conseguiu conectar em {url}")
        print("Verifique se o n8n esta rodando e o workflow esta ativo.")
        return None


def main():
    print(f"\n=== ContaBot — Teste Local de Webhook ===\n")
    print(f"n8n Base: {N8N_BASE}")
    print()
    print("Escolha o teste:")
    print("  1. Mensagem de texto (Q&A Bot)")
    print("  2. Envio de imagem (Intake)")
    print("  3. Envio de documento PDF (Intake)")
    print("  4. Cadastro de cliente (Admin)")
    print("  5. Texto customizado")

    choice = input("\nEscolha (1-5): ").strip()

    if choice == "1":
        msg = input("Mensagem (ou Enter para padrao): ").strip()
        payload = simulate_text_message(message=msg or "Que documentos preciso pro IR?")
        send_to_webhook("contabot-qa", payload)

    elif choice == "2":
        url = input("URL da imagem (ou Enter para padrao): ").strip()
        payload = simulate_image_message(image_url=url or "https://example.com/nota.jpg")
        send_to_webhook("contabot-intake", payload)

    elif choice == "3":
        url = input("URL do PDF (ou Enter para padrao): ").strip()
        payload = simulate_document_message(doc_url=url or "https://example.com/guia.pdf")
        send_to_webhook("contabot-intake", payload)

    elif choice == "4":
        payload = simulate_cadastro()
        send_to_webhook("contabot-admin", payload)

    elif choice == "5":
        phone = input("Telefone (ex: 5511999999999): ").strip()
        msg = input("Mensagem: ").strip()
        endpoint = input("Endpoint (contabot-intake / contabot-qa / contabot-admin): ").strip()
        payload = simulate_text_message(phone=phone, message=msg)
        send_to_webhook(endpoint, payload)

    else:
        print("Opcao invalida.")


if __name__ == "__main__":
    main()
