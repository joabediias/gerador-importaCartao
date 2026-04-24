from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QStyleFactory

# ============================================================
# PALETA BASE DA APLICAÇÃO
# ============================================================
BG_APP = "#f6f8fb"
BG_CARD = "#ffffff"
BG_SOFT = "#f9fafb"
BG_DISABLED = "#f3f4f6"

TEXT_PRIMARY = "#111827"
TEXT_SECONDARY = "#374151"
TEXT_LIGTH = "#e5e7eb"
TEXT_MUTED = "#6b7280"
TEXT_DISABLED = "#9ca3af"

PRIMARY_RED = "#dc2626"
PRIMARY_RED_HOVER = "#b91c1c"
PRIMARY_RED_PRESSED = "#991b1b"
PRIMARY_RED_LIGHT = "#fee2e2"

SUCCESS_GREEN = "#16a34a"
SUCCESS_GREEN_HOVER = "#15803d"

BORDER_LIGHT = "#d1d5db"
BORDER_CARD = "#e5e7eb"
BORDER_SOFT = "#eef2f7"

HEADER_SUBTITLE = "rgba(255, 255, 255, 0.88)"
HEADER_HELPER = "#fde2e2"

INFO_BG = "#eff6ff"
INFO_BORDER = "#bfdbfe"

SUCCESS_BG = "#ecfdf5"
SUCCESS_BORDER = "#bbf7d0"

WARNING_BG = "#fffbeb"
WARNING_BORDER = "#fde68a"

ERROR_BG = "#fef2f2"
ERROR_BORDER = "#fecaca"


def configure_application(app: QApplication) -> None:
    """Aplica o estilo base do Qt e define a paleta principal da aplicação."""
    app.setStyle(QStyleFactory.create("Fusion"))

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_APP))
    palette.setColor(QPalette.WindowText, QColor(TEXT_SECONDARY))
    palette.setColor(QPalette.Base, QColor(BG_CARD))
    palette.setColor(QPalette.AlternateBase, QColor("#eef4fb"))
    palette.setColor(QPalette.ToolTipBase, QColor(BG_CARD))
    palette.setColor(QPalette.ToolTipText, QColor(TEXT_SECONDARY))
    palette.setColor(QPalette.Text, QColor(TEXT_SECONDARY))
    palette.setColor(QPalette.Button, QColor("#e7f0fb"))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_SECONDARY))
    palette.setColor(QPalette.BrightText, QColor("#ffffff"))
    palette.setColor(QPalette.Highlight, QColor("#dbeeff"))
    palette.setColor(QPalette.HighlightedText, QColor("#10283f"))
    app.setPalette(palette)
