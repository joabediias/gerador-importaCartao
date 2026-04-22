# Estrutura do projeto — Layout ImportaCartão

## Objetivo

A ideia desta versão é manter a aplicação **simples e funcional**, mas com uma estrutura de projeto mais profissional.

O princípio adotado foi separar o sistema em camadas leves:

- **UI**: janelas, widgets, eventos e aparência.
- **Use cases**: fluxo principal da aplicação.
- **Domain**: regras de negócio, constantes, mapeamentos e validações.
- **Services**: leitura de Excel, exportação de CSV/ZIP e acesso a arquivos.
- **Utils**: funções pequenas e reutilizáveis.

## Árvore resumida

```text
layout_importacartao/
├─ desktop_app.py                  # ponto de entrada da aplicação
├─ requirements.txt
├─ README.md
├─ ESTRUTURA_DO_PROJETO.md
├─ assets/                         # logo, banner, ícone
├─ templates/                      # planilha modelo oficial
├─ app/
│  ├─ main.py                      # inicializa QApplication e abre a janela
│  ├─ ui/
│  │  ├─ main_window.py            # janela principal
│  │  ├─ styles.py                 # paleta e stylesheet
│  │  └─ widgets/
│  │     ├─ header_widget.py
│  │     ├─ model_box_widget.py
│  │     ├─ upload_box_widget.py
│  │     ├─ parameters_widget.py
│  │     ├─ summary_widget.py
│  │     └─ output_tabs_widget.py
│  ├─ use_cases/
│  │  └─ generate_files.py         # coordena leitura, validação e geração
│  ├─ domain/
│  │  ├─ constants.py              # nomes, caminhos e configs do app
│  │  ├─ models.py                 # dataclasses da aplicação
│  │  ├─ mappings.py               # códigos de bandeiras, rede, retenção
│  │  └─ validators.py             # validações da planilha e dos parâmetros
│  ├─ services/
│  │  ├─ excel_service.py          # leitura da aba TAXAS
│  │  ├─ generation_service.py     # geração dos 4 dataframes
│  │  ├─ export_service.py         # salvar CSVs e ZIP
│  │  └─ template_service.py       # salvar cópia do modelo
│  └─ utils/
│     └─ parsing.py                # normalização de texto, números e listas
└─ tests/
   └─ test_smoke_structure.py      # teste simples de sanidade
```

## Como essa estrutura ajuda

### 1. UI separada da regra

A janela não precisa mais conhecer detalhe de mapeamento de bandeira, CSV ou planilha. Ela apenas coleta os parâmetros e chama um caso de uso.

### 2. Regras de negócio centralizadas

Mapeamentos como `VISA -> VIS` e `CIELO -> C` ficam num lugar só, evitando strings espalhadas pelo projeto inteiro.

### 3. Facilidade para evoluir o visual

Como os widgets estão separados, fica muito mais fácil mexer em aparência sem tocar na geração dos arquivos.

### 4. Facilidade para testar

A lógica principal pode ser validada fora da interface.

## Fluxo principal da aplicação

1. O usuário baixa ou abre o modelo oficial.
2. Seleciona a planilha preenchida.
3. Informa os parâmetros pela interface.
4. A UI monta um objeto `AppParams`.
5. O use case `generate_import_files` chama os serviços:
   - leitura do Excel
   - extração das taxas
   - geração dos dataframes
   - geração opcional do ZIP
6. A UI exibe resumos, tabelas e permite exportar os arquivos.

## Padrão prático adotado

Não foi usada uma arquitetura pesada demais. A proposta aqui é um padrão de mercado **bem organizado**, mas ainda fácil de manter por uma equipe pequena ou até uma pessoa só.

## Onde mexer no dia a dia

- **Aparência**: `app/ui/styles.py`
- **Campos da tela**: `app/ui/widgets/parameters_widget.py`
- **Layout da janela**: `app/ui/main_window.py`
- **Regras dos arquivos gerados**: `app/services/generation_service.py`
- **Mapeamentos**: `app/domain/mappings.py`
- **Validações**: `app/domain/validators.py`

## Próximas evoluções recomendadas

- logs mais detalhados
- testes automatizados mais completos
- preview com filtros
- histórico de geração
- preferências salvas do usuário
- empacotamento com ícone `.ico`
