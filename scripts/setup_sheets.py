"""
ContaBot — Setup Google Sheets
Cria a planilha com 5 abas, headers e formatacao condicional.
"""
import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

ESCRITORIO = os.getenv("ESCRITORIO_NOME", "Contabilidade XYZ")
SA_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "./credentials/service-account.json")


def get_client():
    creds = Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def create_spreadsheet(gc):
    title = f"ContaBot — {ESCRITORIO}"
    sh = gc.create(title)
    print(f"Planilha criada: {title}")
    print(f"ID: {sh.id}")
    print(f"URL: {sh.url}")
    return sh


def setup_clientes(sh):
    ws = sh.sheet1
    ws.update_title("CLIENTES")
    headers = [
        "ID", "Nome", "CPF/CNPJ", "WhatsApp", "Email",
        "Tipo", "Status", "Pasta Drive", "Data Cadastro", "Observacoes"
    ]
    ws.update("A1:J1", [headers])
    ws.format("A1:J1", {
        "backgroundColor": {"red": 0.26, "green": 0.15, "blue": 0.46},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })
    ws.freeze(rows=1)
    ws.set_basic_filter()

    # Validacao: Tipo
    ws.add_validation(
        "F2:F1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        ["PF", "MEI", "PJ Simples", "PJ Presumido", "PJ Real"],
        strict=True, showCustomUi=True
    )
    # Validacao: Status
    ws.add_validation(
        "G2:G1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        ["Ativo", "Inativo", "Pendente Cadastro"],
        strict=True, showCustomUi=True
    )

    # Formatacao condicional
    rules = ws.conditional_format_rules
    rules.clear()

    # Ativo = verde
    rule_ativo = gspread.worksheet.ConditionalFormatRule(
        ranges=[gspread.worksheet.GridRange.from_a1_range("A2:J1000", ws)],
        booleanRule=gspread.worksheet.BooleanRule(
            condition=gspread.worksheet.BooleanCondition("CUSTOM_FORMULA", ['=$G2="Ativo"']),
            format=gspread.worksheet.CellFormat(backgroundColor=gspread.worksheet.Color(0.85, 0.95, 0.85))
        )
    )
    # Inativo = cinza
    rule_inativo = gspread.worksheet.ConditionalFormatRule(
        ranges=[gspread.worksheet.GridRange.from_a1_range("A2:J1000", ws)],
        booleanRule=gspread.worksheet.BooleanRule(
            condition=gspread.worksheet.BooleanCondition("CUSTOM_FORMULA", ['=$G2="Inativo"']),
            format=gspread.worksheet.CellFormat(backgroundColor=gspread.worksheet.Color(0.9, 0.9, 0.9))
        )
    )
    rules.append(rule_ativo)
    rules.append(rule_inativo)
    rules.save()

    ws.columns_auto_resize(0, 10)
    print("  aba CLIENTES criada")


def setup_documentos(sh):
    ws = sh.add_worksheet("DOCUMENTOS", rows=1000, cols=13)
    headers = [
        "ID", "Data Recebido", "Cliente ID", "Cliente Nome", "Tipo Doc",
        "Subtipo", "Valor", "Competencia", "CNPJ/CPF Emissor",
        "Arquivo Drive", "Confianca IA", "Status", "Observacoes"
    ]
    ws.update("A1:M1", [headers])
    ws.format("A1:M1", {
        "backgroundColor": {"red": 0.26, "green": 0.15, "blue": 0.46},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })
    ws.freeze(rows=1)
    ws.set_basic_filter()

    # Validacao: Tipo Doc
    tipos = [
        "informe_rendimento", "nota_fiscal", "recibo_medico", "recibo_educacao",
        "extrato_bancario", "guia_tributo", "comprovante_pagamento",
        "contrato", "holerite", "certidao", "procuracao", "outro"
    ]
    ws.add_validation("E2:E1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        tipos, strict=True, showCustomUi=True)

    # Validacao: Status
    ws.add_validation("L2:L1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        ["Processado", "Revisar", "Erro"], strict=True, showCustomUi=True)

    ws.columns_auto_resize(0, 13)
    print("  aba DOCUMENTOS criada")


def setup_pendencias(sh):
    ws = sh.add_worksheet("PENDENCIAS", rows=1000, cols=12)
    headers = [
        "ID", "Cliente ID", "Cliente Nome", "WhatsApp", "Tipo",
        "Descricao", "Prazo", "Status", "Ultimo Contato",
        "Tentativas", "Criado Por", "Data Resolucao"
    ]
    ws.update("A1:L1", [headers])
    ws.format("A1:L1", {
        "backgroundColor": {"red": 0.26, "green": 0.15, "blue": 0.46},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })
    ws.freeze(rows=1)
    ws.set_basic_filter()

    ws.add_validation("E2:E1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        ["documento_faltando", "guia_vencendo", "pagamento_atrasado", "checklist_incompleto"],
        strict=True, showCustomUi=True)

    ws.add_validation("H2:H1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        ["Pendente", "Em Cobranca", "Resolvido", "Cancelado"],
        strict=True, showCustomUi=True)

    ws.columns_auto_resize(0, 12)
    print("  aba PENDENCIAS criada")


def setup_guias(sh):
    ws = sh.add_worksheet("GUIAS", rows=1000, cols=12)
    headers = [
        "ID", "Cliente ID", "Cliente Nome", "Tipo", "Competencia",
        "Vencimento", "Valor", "Codigo Barras", "Arquivo Drive",
        "Status", "Data Envio WA", "Data Confirmacao"
    ]
    ws.update("A1:L1", [headers])
    ws.format("A1:L1", {
        "backgroundColor": {"red": 0.26, "green": 0.15, "blue": 0.46},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })
    ws.freeze(rows=1)
    ws.set_basic_filter()

    ws.add_validation("D2:D1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        ["DAS", "DARF", "ISS", "GPS", "FGTS", "IPTU", "IPVA", "IRPF", "Outro"],
        strict=True, showCustomUi=True)

    ws.add_validation("J2:J1000",
        gspread.worksheet.ValidationConditionType.one_of_list,
        ["A Enviar", "Enviado", "Pago", "Vencido"],
        strict=True, showCustomUi=True)

    ws.columns_auto_resize(0, 12)
    print("  aba GUIAS criada")


def setup_config(sh):
    ws = sh.add_worksheet("CONFIG", rows=20, cols=3)
    headers = ["Chave", "Valor", "Descricao"]
    data = [
        headers,
        ["escritorio_nome", os.getenv("ESCRITORIO_NOME", ""), "Nome exibido nas mensagens"],
        ["contador_nome", os.getenv("CONTADOR_NOME", ""), "Nome do responsavel"],
        ["contador_whatsapp", os.getenv("CONTADOR_WHATSAPP", ""), "Numero para escaladas"],
        ["uazapi_instance", os.getenv("UAZAPI_INSTANCE", ""), "Instancia UazAPI"],
        ["drive_folder_id", "", "ID da pasta raiz no Drive"],
        ["sheets_id", sh.id, "ID desta planilha"],
        ["lembrete_intervalo_dias", "3", "Dias entre lembretes"],
        ["max_tentativas", "3", "Maximo de lembretes"],
        ["horario_inicio", "08:00", "Inicio dos envios"],
        ["horario_fim", "18:00", "Fim dos envios"],
        ["irpf_inicio", "01/03/2026", "Inicio temporada IR"],
        ["irpf_fim", "31/05/2026", "Fim temporada IR"],
    ]
    ws.update("A1:C13", data)
    ws.format("A1:C1", {
        "backgroundColor": {"red": 0.26, "green": 0.15, "blue": 0.46},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })
    ws.format("A2:A13", {"textFormat": {"bold": True}})
    ws.columns_auto_resize(0, 3)
    print("  aba CONFIG criada")


def main():
    print(f"\n=== ContaBot — Setup Google Sheets ===")
    print(f"Escritorio: {ESCRITORIO}\n")

    gc = get_client()
    sh = create_spreadsheet(gc)

    setup_clientes(sh)
    setup_documentos(sh)
    setup_pendencias(sh)
    setup_guias(sh)
    setup_config(sh)

    # Compartilhar com email do contador (se quiser)
    # sh.share("email@escritorio.com", perm_type="user", role="writer")

    print(f"\nPlanilha pronta!")
    print(f"ID: {sh.id}")
    print(f"URL: {sh.url}")
    print(f"\nAdicione este ID no .env como CONTABOT_SHEETS_ID={sh.id}")


if __name__ == "__main__":
    main()
