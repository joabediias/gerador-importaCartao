from __future__ import annotations

from .palette import HEADER_HELPER, HEADER_SUBTITLE, PRIMARY_RED


def build_header_styles() -> str:
    return f"""
    /* =======================================================
       HEADER PRINCIPAL
       ======================================================= */
    QFrame#headerCard {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {PRIMARY_RED}, stop:1 #f04438);
        border-radius: 22px;
    }}

    QFrame#headerIconBox {{
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.16);
        border-radius: 18px;
    }}

    QFrame#headerVersionBox {{
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 16px;
    }}

    QLabel#headerIcon {{
        background: transparent;
    }}

    QLabel#heroTitle {{
        color: white;
        font-size: 28px;
        font-weight: 700;
        background: transparent;
    }}

    QLabel#heroSubtitle {{
        color: {HEADER_SUBTITLE};
        font-size: 14px;
        font-weight: 600;
        background: transparent;
    }}

    QLabel#heroHelper {{
        color: {HEADER_HELPER};
        font-size: 12px;
        background: transparent;
    }}

    QLabel#headerVersionTitle {{
        color: white;
        font-size: 14px;
        font-weight: 700;
        background: transparent;
    }}

    QLabel#headerVersionSub {{
        color: {HEADER_HELPER};
        font-size: 12px;
        background: transparent;
    }}
    """
