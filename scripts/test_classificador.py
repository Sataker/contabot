"""
ContaBot — Teste do Classificador
Testa o prompt de classificacao do Claude com uma imagem local ou URL.
"""
import os
import sys
import base64
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

PROMPT_CLASSIFICADOR = """Voce e um assistente especializado em contabilidade brasileira. Analise o documento enviado e retorne um JSON estruturado.

TIPOS DE DOCUMENTO (use exatamente estes valores):
- informe_rendimento
- nota_fiscal
- recibo_medico
- recibo_educacao
- extrato_bancario
- guia_tributo
- comprovante_pagamento
- contrato
- holerite
- certidao
- procuracao
- outro

Extraia os dados com maxima precisao. Se um campo nao for identificavel, use null.
Para valores monetarios, use formato brasileiro (1.234,56). Para datas, use DD/MM/AAAA.

Responda APENAS com JSON valido:
{
  "tipo": "string",
  "subtipo": "string",
  "confianca": 0.0-1.0,
  "dados": {
    "valor_principal": "string ou null",
    "data_documento": "string ou null",
    "competencia": "string ou null",
    "data_vencimento": "string ou null",
    "cnpj_cpf_emissor": "string ou null",
    "nome_emissor": "string ou null",
    "cnpj_cpf_destinatario": "string ou null",
    "nome_destinatario": "string ou null",
    "codigo_barras": "string ou null",
    "numero_documento": "string ou null"
  },
  "resumo": "string (1 linha PT-BR)",
  "requer_revisao": true/false,
  "motivo_revisao": "string ou null"
}"""


def classify_image(image_path):
    """Classifica uma imagem local usando Claude Vision."""
    client = anthropic.Anthropic()

    # Le e codifica a imagem
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Detecta tipo
    ext = image_path.lower().split(".")[-1]
    media_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "pdf": "application/pdf",
    }
    media_type = media_types.get(ext, "image/jpeg")

    message = client.messages.create(
        model="claude-sonnet-4-5-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": PROMPT_CLASSIFICADOR,
                    },
                ],
            }
        ],
    )

    return message.content[0].text


def main():
    if len(sys.argv) < 2:
        print("Uso: python test_classificador.py <caminho-da-imagem>")
        print("\nExemplo:")
        print("  python test_classificador.py nota_fiscal.jpg")
        print("  python test_classificador.py informe_rendimento.pdf")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Arquivo nao encontrado: {image_path}")
        sys.exit(1)

    print(f"\n=== ContaBot — Teste do Classificador ===")
    print(f"Arquivo: {image_path}")
    print(f"Tamanho: {os.path.getsize(image_path) / 1024:.1f} KB")
    print(f"\nClassificando...\n")

    response = classify_image(image_path)

    # Tenta parsear JSON
    try:
        clean = response.replace("```json\n", "").replace("```\n", "").replace("```", "").strip()
        parsed = json.loads(clean)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))

        print(f"\n--- Resumo ---")
        print(f"Tipo: {parsed['tipo']}")
        print(f"Subtipo: {parsed['subtipo']}")
        print(f"Confianca: {parsed['confianca']:.0%}")
        print(f"Valor: {parsed['dados'].get('valor_principal', 'N/A')}")
        print(f"Data: {parsed['dados'].get('data_documento', 'N/A')}")
        print(f"Emissor: {parsed['dados'].get('nome_emissor', 'N/A')}")
        print(f"Revisao: {'SIM' if parsed['requer_revisao'] else 'NAO'}")
        if parsed.get("motivo_revisao"):
            print(f"Motivo: {parsed['motivo_revisao']}")

    except json.JSONDecodeError:
        print("Resposta bruta (nao foi possivel parsear JSON):")
        print(response)


if __name__ == "__main__":
    main()
