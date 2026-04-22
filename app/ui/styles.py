from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QStyleFactory


def configure_application(app: QApplication) -> None:
    app.setStyle(QStyleFactory.create("Fusion"))

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#f4f7fb"))
    palette.setColor(QPalette.WindowText, QColor("#14314d"))
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.AlternateBase, QColor("#eef4fb"))
    palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
    palette.setColor(QPalette.ToolTipText, QColor("#14314d"))
    palette.setColor(QPalette.Text, QColor("#14314d"))
    palette.setColor(QPalette.Button, QColor("#e7f0fb"))
    palette.setColor(QPalette.ButtonText, QColor("#14314d"))
    palette.setColor(QPalette.BrightText, QColor("#ffffff"))
    palette.setColor(QPalette.Highlight, QColor("#dbeeff"))
    palette.setColor(QPalette.HighlightedText, QColor("#10283f"))
    app.setPalette(palette)


def build_stylesheet() -> str:
    return """
    QWidget {
        font-family: 'Segoe UI';
        font-size: 13px;
        color: #14314d;
        background: #f4f7fb;
    }
    QMainWindow, QWidget#page {
        background: #f4f7fb;
    }
    QFrame#headerCard {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #0d4b87, stop:1 #0d876b);
        border-radius: 18px;
    }
    QLabel#heroTitle { color: white; font-size: 26px; font-weight: 700; background: transparent; }
    QLabel#heroSubtitle { color: #edf6ff; font-size: 14px; background: transparent; }
    QLabel#heroHelper { color: #d9ebff; font-size: 12px; background: transparent; }
    QLabel#badge, QLabel#statusPill {
        color: white;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.20);
        border-radius: 14px;
        padding: 6px 12px;
        font-weight: 600;
    }
    QGroupBox {
        font-weight: 700;
        border: 1px solid #d8e4f2;
        border-radius: 14px;
        margin-top: 12px;
        padding: 18px 16px 16px 16px;
        background: #ffffff;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 4px;
        color: #174165;
    }
    QLineEdit, QComboBox, QSpinBox, QTextEdit, QTableWidget {
        background: #ffffff;
        color: #14314d;
        border: 1px solid #c8d8ea;
        border-radius: 8px;
        padding: 6px 8px;
        min-height: 28px;
    }
    QComboBox QAbstractItemView {
        background: #ffffff;
        color: #14314d;
        selection-background-color: #dbeeff;
        selection-color: #10283f;
    }
    QTableWidget::item { color: #16324f; }
    QPushButton {
        background: #edf4fb;
        color: #14314d;
        border: 1px solid #c7d8eb;
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 600;
    }
    QPushButton:hover { background: #e1eefc; }
    QPushButton#primaryButton {
        background: #0e5ea8;
        color: white;
        border-color: #0e5ea8;
    }
    QPushButton#primaryButton:hover { background: #0a4d8c; }
    QLabel#mutedText { color: #5e7690; }
    QLabel#metricValue { font-size: 28px; font-weight: 700; color: #0d4b87; }
    QLabel#metricLabel { color: #5d7590; }
    QScrollArea {
    background: transparent;
    border: none;
    }
    QScrollArea > QWidget > QWidget {
        background: transparent;
    }

    QScrollBar:vertical {
        background: #edf4fb;
        width: 12px;
        margin: 0;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background: #c2d7ee;
        min-height: 30px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical:hover {
        background: #aac8e7;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0;
    }

    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: transparent;
    }
    QCheckBox {
    color: #14314d;
    spacing: 8px;
    background: transparent;
    }

    QCheckBox::indicator {
        width: 16px;
        height: 16px;
    }
    """
