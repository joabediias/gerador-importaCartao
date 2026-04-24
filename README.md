# Layout ImportaCartão

Aplicação desktop em **Python + PySide6** para transformar a planilha oficial de taxas em 4 arquivos CSV:

- `portadores.csv`
- `cartoes.csv`
- `prazos.csv`
- `retencoes.csv`

## Requisitos

- Python 3.11+ recomendado
- Windows 10/11

## Como executar em desenvolvimento

```bash
pip install -r requirements.txt
python desktop_app.py
```

## Como gerar executável

Instale o PyInstaller:

```bash
pip install pyinstaller
```

Gere a pasta do executável:

```bash
python -m PyInstaller --noconfirm --clean --windowed --onedir --add-data "templates/modelo_taxas_cartao.xlsx;templates" --add-data "assets;assets" desktop_app.py
```

O executável será criado em:

```bash
dist\desktop_app\desktop_app.exe
```

## Observações

- O modelo Excel precisa acompanhar a aplicação.
- Os parâmetros gerais são informados na própria tela do sistema.
- A aba `TAXAS` é a fonte dos dados variáveis.
- O campo `EMPRESAS` aceita múltiplos códigos no formato `1;2;3`.
- Se `TIPO_RECEBIMENTO = AMBOS`, o sistema gera um registro `POS` e outro `TEF` para cada cartão.

## Estrutura

- `desktop_app.py` -> interface desktop
- `core.py` -> regras de negócio e geração dos CSVs
- `modelo_taxas_cartao_melhorado.xlsx` -> modelo oficial para preenchimento
