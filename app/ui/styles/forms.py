from __future__ import annotations
from app.utils.resource_path import resource_path

from .palette import (
    BG_CARD,
    BG_SOFT,
    BORDER_CARD,
    BORDER_LIGHT,
    TEXT_LIGTH,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,

)

def build_form_styles() -> str:
    check_icon = resource_path("assets/icons/check.svg")

    return f"""
    /* =======================================================
       INPUTS / COMBOBOX / TABELAS
       ======================================================= */

    QLabel#formLabel {{
        color: {TEXT_PRIMARY};
        font-size: 13px;
        font-weight: 600;
        background: transparent;
    }}

    QLabel#fieldHelp {{
        color: {TEXT_MUTED};
        font-size: 12px;
        background: transparent;
    }}

    QLineEdit,
    QSpinBox,
    QTextEdit,
    QPlainTextEdit {{
        background: {BG_CARD};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 12px;
        padding: 8px 10px;
        min-height: 18px;
    }}

    QLineEdit:hover,
    QSpinBox:hover,
    QTextEdit:hover,
    QPlainTextEdit:hover {{
        border: 1px solid #9ca3af;
    }}

    QLineEdit:focus,
    QSpinBox:focus,
    QTextEdit:focus,
    QPlainTextEdit:focus {{
        background: {BG_CARD};
    }}

    QLineEdit:disabled,
    QSpinBox:disabled,
    QTextEdit:disabled,
    QPlainTextEdit:disabled,
    QComboBox:disabled {{
        background: #f3f4f6;
        color: #9ca3af;
        border: 1px solid #e5e7eb;
    }}

    QSpinBox::up-button,
    QSpinBox::down-button {{
        width: 0px;
        border: none;
    }}

    QSpinBox::up-arrow,
    QSpinBox::down-arrow {{
        image: none;
    }}

    QComboBox {{
        background: {BG_CARD};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 12px;
        padding: 8px 28px 8px 10px;
        min-height: 18px;
        font-size: 13px;
    }}

    QComboBox:hover {{
        border: 1px solid #9ca3af;
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 26px;
        border: none;
        background: transparent;
    }}

    QComboBox::down-arrow {{
        width: 10px;
        height: 10px;
    }}

    QComboBox QAbstractItemView {{
        background: {BG_CARD};
        color: {TEXT_PRIMARY};
        border-radius: 10px;
        padding: 6px;
        outline: 0;
        border: none;
        background: transparent;
        selection-color: {TEXT_PRIMARY};
    }}

    QComboBox QAbstractItemView::item {{
        min-height: 28px;
        padding: 6px 10px;
        border-radius: 6px;
        background: transparent;
        margin: 2px;
    }}

    QComboBox QAbstractItemView::item:selected {{
        background: #e5e7eb;
        color: {TEXT_PRIMARY};
    }}

    QComboBox QAbstractItemView::item:hover {{
        background: #f3f4f6;
        color: {TEXT_PRIMARY};
    }}

    QWidget#customCombo {{
        background: transparent;
    }}

    QPushButton#customComboDisplay {{
        background: #ffffff;
        color: #111827;
        border: 1px solid #d1d5db;
        border-radius: 12px;
        padding: 8px 12px;
        min-height: 20px;
        text-align: left;
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton#customComboDisplay:hover {{
        border: 1px solid #9ca3af;
        background: #ffffff;
    }}

    QPushButton#customComboDisplay:pressed {{
        background: #f9fafb;
    }}

    QFrame#customComboPopup {{
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
    }}

    QListWidget#customComboList {{
        background: transparent;
        border: none;
        outline: 0;
        padding: 0px;
    }}

    QListWidget#customComboList::item {{
        min-height: 28px;
        padding: 6px 10px;
        margin: 2px;
        border-radius: 6px;
        color: #111827;
    }}

    QListWidget#customComboList::item:selected {{
        background: #f3f4f6;
        color: #111827;
    }}

    QListWidget#customComboList::item:hover {{
        background: #f9fafb;
        color: #111827;
    }}
    
    QCheckBox {{
        color: {TEXT_PRIMARY};
        spacing: 8px;
        background: transparent;
        font-size: 13px;
    }}

    /* Caixa (quadrado) */
    QCheckBox::indicator {{
        width: 14px;
        height: 14px;
        border-radius: 4px;
        border: 1px solid #9ca3af;
        background: #ffffff;
    }}

    QCheckBox::indicator:hover {{
        border: 1px solid #6b7280;
    }}

    QCheckBox::indicator:checked {{
        background: #ffffff;
        image: url("{check_icon}");
    }}

    QCheckBox::indicator:checked:hover {{
        border: 1px solid #1d4ed8;
        background: #f8fafc;
    }}

    QTableWidget {{
        background: {BG_CARD};
        alternate-background-color: {BG_SOFT};
        gridline-color: #eef2f7;
        border-radius: 12px;
        color: {TEXT_PRIMARY};
        selection-background-color: {TEXT_LIGTH};
    }}

    QHeaderView::section {{
        background: {BG_SOFT};
        color: {TEXT_SECONDARY};
        border: none;
        border-bottom: 1px solid {BORDER_CARD};
        padding: 10px 8px;
        font-weight: 700;
    }}
    """