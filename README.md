# ContaBot

Sistema de automacao para escritorios de contabilidade. Integra WhatsApp (UazAPI) + Google Drive + Google Sheets + Claude API via n8n.

## O que faz

- Recebe documentos do cliente via WhatsApp, classifica com IA e salva organizado no Drive
- Envia guias de pagamento automaticamente todo mes
- Cobra documentos pendentes com lembretes escalonados
- Responde duvidas simples do cliente via WhatsApp (escala as complexas pro contador)
- Envia checklist do IRPF automaticamente na temporada (marco-maio)
- Cadastra novos clientes via mensagem do contador

## Stack

- **n8n** — orquestracao de workflows (self-hosted)
- **UazAPI** — API de WhatsApp (spark.uazapi.com)
- **Claude API** — classificacao de documentos (Vision) e Q&A (Haiku)
- **Google Drive** — armazenamento de documentos
- **Google Sheets** — banco de dados + dashboard

## Estrutura

```
contabot/
├── config/
│   ├── config.example.json       # Template de configuracao
│   └── prompts/
│       ├── classificador.md      # Prompt de classificacao de docs
│       ├── qa-bot.md             # Prompt Q&A do cliente
│       └── escalador.md          # Regras de escalada
├── workflows/
│   ├── 01-intake-documentos.json
│   ├── 02-comunicacao-agendada.json
│   ├── 03-qa-bot.json
│   ├── 04-irpf-checklist.json
│   └── 05-admin-cadastro.json
├── sheets/
│   └── template-descricao.md
└── docs/
    ├── ONBOARDING.md
    └── DRIVE-STRUCTURE.md
```

## Workflows

| # | Nome | Trigger | Funcao |
|---|------|---------|--------|
| 01 | Intake de Documentos | Webhook (imagem/PDF via WhatsApp) | Classifica, salva no Drive, loga na Sheets |
| 02 | Comunicacao Agendada | Cron (9h dias uteis) | Envia guias + cobra pendencias |
| 03 | Q&A Bot | Webhook (texto via WhatsApp) | Responde duvidas ou escala pro contador |
| 04 | IRPF Checklist | Cron (1o dia mar/abr/mai) | Envia checklist + lembretes do IR |
| 05 | Admin Cadastro | Webhook (msg do contador) | Cadastra cliente novo |

## Deploy

Ver `docs/ONBOARDING.md` para o checklist completo de ativacao.

Resumo:
1. Configurar UazAPI (instancia + webhook)
2. Criar pasta raiz no Google Drive
3. Criar planilha Google Sheets com 5 abas
4. Setar variaveis de ambiente no n8n
5. Importar os 5 workflows
6. Cadastrar clientes
7. Testar

## Custo de Infra

- n8n: ja existente (self-hosted)
- UazAPI: ~R$30-50/mes
- Claude API: ~R$20-50/mes (depende do volume)
- Google Workspace: ~R$27/mes (se precisar de mais storage)
- VPS: ja existente

**Total: ~R$50-130/mes por escritorio**

## Precificacao Sugerida

- Setup: R$3.000 - R$5.000
- Mensalidade: R$500 - R$900/mes
- Margem liquida: R$400 - R$800/mes por cliente
