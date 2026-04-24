from pathlib import Path

APP_NAME = "Layout Importa Cartão"
APP_SUBTITLE = "Gerador local de arquivos CSV para importação de cartões"
APP_VERSION = "1.0.5"

BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = BASE_DIR / "templates"

LOGO_PATH = ASSETS_DIR / "logo.png"
ICON_APP_CARD = ASSETS_DIR / "app_card.svg"
TEMPLATE_PATH = TEMPLATES_DIR / "modelo_taxas_cartao.xlsx"

CSV_SEPARATOR = ";"
CSV_ENCODING = "utf-8-sig"