# Checklist de Onboarding — ContaBot

Guia passo a passo para ativar o ContaBot em um novo escritorio de contabilidade.

---

## PRE-REQUISITOS DO ESCRITORIO

- [ ] Numero de WhatsApp dedicado (nao usar pessoal do contador)
- [ ] Conta Google Workspace (ou Gmail com Drive)
- [ ] Lista de clientes ativos (nome, CPF/CNPJ, WhatsApp)
- [ ] Certificado digital do escritorio (para acessos futuros)

---

## ETAPA 1 — CONFIGURACAO UAZAPI (30 min)

- [ ] Criar instancia no painel UazAPI
- [ ] Conectar numero de WhatsApp via QR Code
- [ ] Anotar o token da instancia
- [ ] Configurar webhook apontando para: `https://[seu-n8n]/webhook/contabot-intake`
- [ ] Testar envio de mensagem via API

---

## ETAPA 2 — GOOGLE DRIVE (20 min)

- [ ] Criar pasta raiz: `ContaBot — [Nome do Escritorio]`
- [ ] Dentro da raiz, criar pasta `CLIENTES`
- [ ] Compartilhar pasta raiz com a Service Account do Google Cloud
- [ ] Anotar o ID da pasta raiz (na URL do Drive, depois de `/folders/`)

---

## ETAPA 3 — GOOGLE SHEETS (30 min)

- [ ] Criar planilha: `ContaBot — [Nome do Escritorio]`
- [ ] Criar 5 abas conforme template: CLIENTES, DOCUMENTOS, PENDENCIAS, GUIAS, CONFIG
- [ ] Adicionar headers em cada aba (conforme sheets/template-descricao.md)
- [ ] Preencher aba CONFIG com dados do escritorio
- [ ] Adicionar formatacao condicional (cores por status)
- [ ] Compartilhar planilha com a Service Account
- [ ] Anotar o ID da planilha (na URL, entre `/d/` e `/edit`)

---

## ETAPA 4 — VARIAVEIS DE AMBIENTE N8N (10 min)

Configurar no n8n (Settings > Environment Variables):

```
CONTABOT_SHEETS_ID=ID_DA_PLANILHA
CONTABOT_DRIVE_FOLDER_ID=ID_DA_PASTA_DRIVE
UAZAPI_BASE_URL=https://spark.uazapi.com
UAZAPI_TOKEN=TOKEN_DA_INSTANCIA
CLAUDE_API_KEY=sk-ant-CHAVE
CONTADOR_WHATSAPP=5511999999999
```

---

## ETAPA 5 — IMPORTAR WORKFLOWS (15 min)

- [ ] Importar `01-intake-documentos.json` no n8n
- [ ] Importar `02-comunicacao-agendada.json`
- [ ] Importar `03-qa-bot.json`
- [ ] Importar `04-irpf-checklist.json`
- [ ] Importar `05-admin-cadastro.json`
- [ ] Configurar credenciais Google (Drive + Sheets) em cada workflow
- [ ] Ativar todos os workflows

---

## ETAPA 6 — CADASTRAR CLIENTES (variavel)

Duas opcoes:

**Opcao A — Via planilha (mais rapido para muitos clientes):**
- [ ] Preencher aba CLIENTES manualmente com todos os clientes ativos
- [ ] Criar pastas no Drive para cada cliente (pode ser manual ou via script)

**Opcao B — Via WhatsApp (um por um):**
- [ ] Enviar mensagem formatada do numero do contador:
```
NOVO_CLIENTE
Nome: Joao Silva
CPF: 123.456.789-00
WhatsApp: 11999999999
Tipo: PF
```

---

## ETAPA 7 — TESTES (30 min)

- [ ] Enviar foto de nota fiscal de teste no WhatsApp → verificar classificacao + Drive + Sheets
- [ ] Enviar foto de informe de rendimento → verificar classificacao
- [ ] Enviar mensagem de texto "que documentos preciso pro IR?" → verificar resposta do bot
- [ ] Enviar pergunta complexa "quanto vou pagar de imposto?" → verificar escalada pro contador
- [ ] Adicionar guia teste na aba GUIAS com status "A Enviar" → executar WF02 manualmente → verificar envio
- [ ] Adicionar pendencia teste na aba PENDENCIAS → executar WF02 → verificar lembrete
- [ ] Cadastrar cliente teste via WhatsApp do contador → verificar Sheets + Drive

---

## ETAPA 8 — TREINAMENTO (1h)

- [ ] Treinar contador para usar a planilha (adicionar guias, pendencias)
- [ ] Treinar para cadastrar clientes via WhatsApp
- [ ] Explicar como funciona a classificacao automatica
- [ ] Explicar o fluxo de escalada (quando o bot encaminha pro contador)
- [ ] Explicar aba CONFIG (alterar mensagens, horarios)
- [ ] Definir quem revisa documentos com flag "Revisar"

---

## POS-ATIVACAO

- [ ] Monitorar primeiras 48h de operacao
- [ ] Ajustar prompts do Claude se classificacao estiver errando
- [ ] Coletar feedback do contador e dos clientes
- [ ] Agendar revisao em 7 dias
