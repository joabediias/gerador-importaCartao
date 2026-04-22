from pathlib import Path

APP_NAME = "Layout ImportaCartão"
APP_SUBTITLE = "Gerador local de arquivos CSV para importação de cartões"
APP_VERSION = "1.0.3-structured"

BASE_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATES_DIR = BASE_DIR / "templates"

LOGO_PATH = ASSETS_DIR / "logo_importacartao.png"
BANNER_PATH = ASSETS_DIR / "banner_importacartao.png"
TEMPLATE_PATH = TEMPLATES_DIR / "modelo_taxas_cartao_melhorado.xlsx"

CSV_SEPARATOR = ";"
CSV_ENCODING = "utf-8-sig"
