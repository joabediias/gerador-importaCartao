from __future__ import annotations

from .palette import ERROR_BG, ERROR_BORDER, SUCCESS_GREEN, SUCCESS_BG, SUCCESS_BORDER


def build_feedback_styles() -> str:
    return f"""
    /* =======================================================
       ALERTAS / BANNERS / PROGRESSO
       ======================================================= */
    QFrame#alertBanner_success {{
        background: {SUCCESS_BG};
        border: 1px solid {SUCCESS_BORDER};
        border-radius: 14px;
    }}

    QFrame#alertBanner_error {{
        background: {ERROR_BG};
        border: 1px solid {ERROR_BORDER};
        border-radius: 14px;
    }}

    QLabel#alertText {{
        font-size: 13px;
        font-weight: 600;
        background: transparent;
    }}

    QFrame#alertBanner_success QLabel#alertText {{
        color: #166534;
    }}

    QFrame#alertBanner_error QLabel#alertText {{
        color: #991b1b;
    }}

    QProgressBar#mainProgressBar {{
        background: #f3f4f6;
        border: none;
        border-radius: 8px;
        text-align: center;
        color: #ffffff;
        min-height: 14px;
        font-weight: 700;
    }}

    QProgressBar#mainProgressBar::chunk {{
        background: {SUCCESS_GREEN};
        border-radius: 8px;
    }}
    """
