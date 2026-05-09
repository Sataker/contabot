# Estrutura de Pastas — Google Drive

Estrutura padrao criada para cada escritorio.

```
ContaBot — [Nome do Escritorio]/
│
├── CLIENTES/
│   │
│   ├── 123.456.789-00 — Joao Silva/
│   │   ├── 2025/
│   │   │   └── IRPF/
│   │   │       ├── informes/
│   │   │       ├── notas-medicas/
│   │   │       ├── educacao/
│   │   │       └── outros/
│   │   └── 2026/
│   │       ├── IRPF/
│   │       │   ├── informes/
│   │       │   ├── notas-medicas/
│   │       │   ├── educacao/
│   │       │   └── outros/
│   │       └── MENSAIS/
│   │           ├── 01-JAN/
│   │           │   ├── guias/
│   │           │   ├── comprovantes/
│   │           │   └── extratos/
│   │           ├── 02-FEV/
│   │           ├── 03-MAR/
│   │           └── ...
│   │
│   ├── 12.345.678/0001-99 — Empresa ABC Ltda/
│   │   └── 2026/
│   │       └── MENSAIS/
│   │           ├── 01-JAN/
│   │           │   ├── notas-fiscais/
│   │           │   ├── guias/
│   │           │   ├── extratos/
│   │           │   └── comprovantes/
│   │           └── ...
│   │
│   └── ... (demais clientes)
│
└── _MODELOS/
    ├── checklist-irpf-pf.pdf
    ├── checklist-documentos-pj.pdf
    └── orientacoes-cliente.pdf
```

## Regras de Nomeacao

- Pasta do cliente: `[CPF ou CNPJ] — [Nome Completo]`
- Arquivos recebidos: `[TIPO]_[DATA]_[ID-CURTO].[ext]`
  - Exemplo: `nota_fiscal_15-03-2026_a1b2c3d4.pdf`
  - Exemplo: `informe_rendimento_01-01-2026_e5f6g7h8.jpg`

## Notas

- O WF01 salva automaticamente na pasta raiz do cliente. Subpastas por mes/tipo podem ser criadas manualmente ou em v2 do sistema.
- Pasta `_MODELOS` contem templates que o escritorio pode enviar aos clientes.
- Compartilhar pasta do cliente com ele (via link) e opcional — depende da politica do escritorio.
