from __future__ import annotations

from .palette import (
    BG_CARD,
    BG_DISABLED,
    BORDER_LIGHT,
    PRIMARY_RED,
    PRIMARY_RED_HOVER,
    PRIMARY_RED_PRESSED,
    SUCCESS_GREEN,
    SUCCESS_GREEN_HOVER,
    TEXT_DISABLED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


def build_button_styles() -> str:
    return f"""
    /* =======================================================
       BOTÕES
       ======================================================= */
    QPushButton {{
        background: {BG_CARD};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 12px;
        padding: 10px 16px;
        min-height: 18px;
        font-size: 13px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background: #f9fafb;
        border: 1px solid #9ca3af;
    }}

    QPushButton:pressed {{
        background: #f3f4f6;
    }}

    QPushButton:disabled {{
        background: {BG_DISABLED};
        color: {TEXT_DISABLED};
        border: 1px solid #e5e7eb;
    }}

    QPushButton#primaryButton {{
        background: {PRIMARY_RED};
        color: white;
        border: 1px solid {PRIMARY_RED};
    }}

    QPushButton#primaryButton:hover {{
        background: {PRIMARY_RED_HOVER};
        border: 1px solid {PRIMARY_RED_HOVER};
    }}

    QPushButton#primaryButton:pressed {{
        background: {PRIMARY_RED_PRESSED};
        border: 1px solid {PRIMARY_RED_PRESSED};
    }}

    QPushButton#successButton {{
        background: {SUCCESS_GREEN};
        color: white;
        border: 1px solid {SUCCESS_GREEN};
    }}

    QPushButton#successButton:hover {{
        background: {SUCCESS_GREEN_HOVER};
        border: 1px solid {SUCCESS_GREEN_HOVER};
    }}

    QPushButton#ghostButton {{
        background: transparent;
        color: {TEXT_SECONDARY};
        border: 1px solid {BORDER_LIGHT};
    }}

    QPushButton#ghostButton:hover {{
        background: #f9fafb;
        border: 1px solid #9ca3af;
    }}
    """