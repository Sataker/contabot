# Google Sheets — Template ContaBot

Criar uma planilha Google Sheets com o nome: **ContaBot — [Nome do Escritorio]**

---

## ABA 1: CLIENTES

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| A — ID | Texto | Identificador unico (ex: CLI-001) |
| B — Nome | Texto | Nome completo do cliente |
| C — CPF/CNPJ | Texto | Documento principal formatado |
| D — WhatsApp | Texto | Formato 5511999999999 (sem +, sem espacos) |
| E — Email | Texto | Email do cliente |
| F — Tipo | Lista suspensa | PF / MEI / PJ Simples / PJ Presumido / PJ Real |
| G — Status | Lista suspensa | Ativo / Inativo / Pendente Cadastro |
| H — Pasta Drive | URL | Link direto para pasta do cliente no Drive |
| I — Data Cadastro | Data | DD/MM/AAAA |
| J — Observacoes | Texto | Notas livres do contador |

**Formatacao condicional:**
- Status "Ativo" = fundo verde claro
- Status "Inativo" = fundo cinza
- Status "Pendente Cadastro" = fundo amarelo

---

## ABA 2: DOCUMENTOS

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| A — ID | Texto | Auto (DOC-001, DOC-002...) |
| B — Data Recebido | Data/hora | Timestamp de quando chegou no WhatsApp |
| C — Cliente ID | Texto | Referencia para aba CLIENTES (CLI-001) |
| D — Cliente Nome | Texto | Nome (desnormalizado pra facilitar leitura) |
| E — Tipo Doc | Lista suspensa | informe_rendimento / nota_fiscal / recibo_medico / recibo_educacao / extrato_bancario / guia_tributo / comprovante_pagamento / contrato / holerite / certidao / procuracao / outro |
| F — Subtipo | Texto | Detalhe livre do Claude (ex: "Informe PJ - Bradesco 2025") |
| G — Valor | Moeda | R$ extraido do documento |
| H — Competencia | Texto | MM/AAAA |
| I — CNPJ/CPF Emissor | Texto | Do documento |
| J — Arquivo Drive | URL | Link direto para o arquivo no Drive |
| K — Confianca IA | Porcentagem | Score do Claude (0% a 100%) |
| L — Status | Lista suspensa | Processado / Revisar / Erro |
| M — Observacoes | Texto | Notas do Claude ou do contador |

**Formatacao condicional:**
- Confianca >= 70% = fundo verde
- Confianca 50-69% = fundo amarelo
- Confianca < 50% = fundo vermelho
- Status "Revisar" = texto vermelho negrito

---

## ABA 3: PENDENCIAS

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| A — ID | Texto | PEN-001, PEN-002... |
| B — Cliente ID | Texto | Referencia |
| C — Cliente Nome | Texto | |
| D — WhatsApp | Texto | Pra facilitar envio |
| E — Tipo | Lista suspensa | documento_faltando / guia_vencendo / pagamento_atrasado / checklist_incompleto |
| F — Descricao | Texto | Ex: "Informe de rendimentos Banco Itau nao enviado" |
| G — Prazo | Data | DD/MM/AAAA |
| H — Status | Lista suspensa | Pendente / Em Cobranca / Resolvido / Cancelado |
| I — Ultimo Contato | Data/hora | Quando mandou o ultimo lembrete |
| J — Tentativas | Numero | Quantos lembretes ja foram enviados (0, 1, 2, 3) |
| K — Criado Por | Texto | Nome do contador que criou a pendencia |
| L — Data Resolucao | Data | Quando foi resolvido |

**Formatacao condicional:**
- Prazo < hoje E Status != Resolvido = linha inteira fundo vermelho
- Prazo < hoje+3 dias = fundo amarelo
- Status "Resolvido" = fundo verde claro, texto cinza

---

## ABA 4: GUIAS

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| A — ID | Texto | GUIA-001, GUIA-002... |
| B — Cliente ID | Texto | Referencia |
| C — Cliente Nome | Texto | |
| D — Tipo | Lista suspensa | DAS / DARF / ISS / GPS / FGTS / IPTU / IPVA / IRPF / Outro |
| E — Competencia | Texto | MM/AAAA |
| F — Vencimento | Data | DD/MM/AAAA |
| G — Valor | Moeda | R$ |
| H — Codigo Barras | Texto | Linha digitavel completa |
| I — Arquivo Drive | URL | Link para PDF da guia |
| J — Status | Lista suspensa | A Enviar / Enviado / Pago / Vencido |
| K — Data Envio WA | Data/hora | Quando foi enviado no WhatsApp |
| L — Data Confirmacao | Data/hora | Quando cliente confirmou pagamento |

**Formatacao condicional:**
- Status "A Enviar" = fundo azul claro
- Status "Enviado" = fundo amarelo
- Status "Pago" = fundo verde
- Status "Vencido" = fundo vermelho negrito

---

## ABA 5: CONFIG

| Chave | Valor | Descricao |
|-------|-------|-----------|
| escritorio_nome | Contabilidade XYZ | Nome nas mensagens |
| escritorio_cnpj | 12.345.678/0001-99 | |
| contador_nome | Dr. Carlos Mendes | Nome do responsavel |
| contador_whatsapp | 5511999988887 | Para escaladas |
| n8n_webhook_url | https://n8n.exemplo.com/webhook/contabot | URL do webhook |
| uazapi_instance | contabilidade-xyz | Instancia UazAPI |
| drive_folder_id | 1abc123... | ID pasta raiz Drive |
| lembrete_intervalo_dias | 3 | Dias entre lembretes |
| max_tentativas | 3 | Maximo de lembretes |
| horario_inicio | 08:00 | Inicio envios |
| horario_fim | 18:00 | Fim envios |
| irpf_inicio | 01/03/2026 | Inicio temporada IR |
| irpf_fim | 31/05/2026 | Fim temporada IR |

---

## FORMULAS UTEIS (adicionar na aba CONFIG ou em aba separada DASHBOARD)

```
Total clientes ativos:
=COUNTIF(CLIENTES!G:G,"Ativo")

Total documentos recebidos (mes atual):
=COUNTIFS(DOCUMENTOS!B:B,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1),DOCUMENTOS!B:B,"<"&DATE(YEAR(TODAY()),MONTH(TODAY())+1,1))

Pendencias abertas:
=COUNTIF(PENDENCIAS!H:H,"Pendente")+COUNTIF(PENDENCIAS!H:H,"Em Cobranca")

Guias vencidas sem pagamento:
=COUNTIFS(GUIAS!F:F,"<"&TODAY(),GUIAS!J:J,"<>"&"Pago")

Documentos para revisao:
=COUNTIF(DOCUMENTOS!L:L,"Revisar")

Taxa de classificacao automatica (sem revisao):
=COUNTIF(DOCUMENTOS!L:L,"Processado")/COUNTA(DOCUMENTOS!L:L)
```
