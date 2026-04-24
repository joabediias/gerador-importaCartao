from __future__ import annotations

from .palette import BG_APP, TEXT_MUTED, TEXT_PRIMARY


def build_base_styles() -> str:
    return f"""
    /* =======================================================
       BASE GLOBAL
       ======================================================= */
    QWidget {{
        font-family: 'Segoe UI';
        font-size: 13px;
        color: {TEXT_PRIMARY};
        background: {BG_APP};
    }}

    QMainWindow, QWidget#page {{
        background: {BG_APP};
    }}

    QWidget#headerLeftWidget,
    QWidget#headerLeftWidget QLabel,
    QWidget#headerLeftWidget QFrame,
    QWidget#headerLeftWidget QWidget {{
        background: transparent;
    }}

    QLabel {{
        color: {TEXT_PRIMARY};
        background: transparent;
    }}

    QLabel#mutedText {{
        color: {TEXT_MUTED};
    }}
    """
