from __future__ import annotations

from .palette import BG_APP, BG_CARD, BORDER_CARD, BORDER_SOFT, PRIMARY_RED


def build_card_styles() -> str:
    return f"""
    /* =======================================================
       CONTAINERS / GROUPBOX / CARDS BASE
       ======================================================= */
    QGroupBox {{
        font-weight: 700;
        color: #1d4f91;
        border: 1px solid {BORDER_CARD};
        border-radius: 16px;
        margin-top: 12px;
        padding: 18px 16px 16px 16px;
        background: {BG_CARD};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 14px;
        padding: 0 6px;
        color: #1d4f91;
        background: {BG_APP};
    }}

    QLabel#metricValue {{
        color: #0f172a;
        font-size: 30px;
        font-weight: 800;
    }}

    QLabel#metricLabel {{
        color: #6f84a0;
        font-size: 12px;
        background: transparent;
        padding: 0;
        margin: 0;
    }}

    QLabel#metricIcon {{
        border-radius: 20px;
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
        background: rgba(255,255,255,0.65);
    }}

    QFrame[class="metricCard"] {{
        background: #ffffff;
        border: 1px solid #e7eaf0;
        border-radius: 16px;
    }}

    QFrame#metricCardBlue {{
        border-top: 4px solid #2563eb;
    }}

    QFrame#metricCardGreen {{
        border-top: 4px solid #16a34a;
    }}

    QFrame#metricCardYellow {{
        border-top: 4px solid #d97706;
    }}

    QFrame#metricCardPurple {{
        border-top: 4px solid #7c3aed;
    }}

    QLabel#metricValue {{
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        padding: 0;
        margin: 0;
    }}

    QLabel#metricLabel {{
        color: #6b7280;
        font-size: 13px;
        font-weight: 600;
        padding: 0;
        margin: 0;
    }}
    """
