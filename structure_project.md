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