from __future__ import annotations

from .palette import BG_CARD, TEXT_MUTED


def build_layout_styles() -> str:
    return f"""
    /* =======================================================
       SCROLL / STATUS / SECTION HEADERS / EMPTY STATE
       ======================================================= */
    QScrollArea {{
        background: transparent;
        border: none;
    }}

    QScrollArea > QWidget > QWidget {{
        background: transparent;
    }}

    QScrollBar:vertical {{
        background: #edf3fa;
        width: 12px;
        margin: 0;
        border-radius: 6px;
    }}

    QScrollBar::handle:vertical {{
        background: #c7d7ea;
        min-height: 30px;
        border-radius: 6px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: #b4cae4;
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0;
    }}

    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {{
        background: transparent;
    }}

    QStatusBar {{
        background: {BG_CARD};
        color: #69809c;
        border-top: 1px solid #e4ebf3;
    }}

    QLabel#sectionTitle {{
        font-size: 15px;
        font-weight: 700;
        color: #000000;
    }}

    QLabel#emptyIcon {{
        font-size: 48px;
    }}

    QLabel#emptyTitle {{
        font-size: 16px;
        font-weight: 700;
        color: #2b4a6f;
    }}

    QLabel#emptySubtitle {{
        font-size: 13px;
        color: {TEXT_MUTED};
    }}
    """
