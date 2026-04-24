from __future__ import annotations

from .base import build_base_styles
from .buttons import build_button_styles
from .cards import build_card_styles
from .feedback import build_feedback_styles
from .forms import build_form_styles
from .header import build_header_styles
from .layout import build_layout_styles
from .palette import configure_application


def build_stylesheet() -> str:
    """Monta o stylesheet global combinando os módulos visuais da UI."""
    return "\n".join(
        [
            build_base_styles(),
            build_header_styles(),
            build_card_styles(),
            build_form_styles(),
            build_button_styles(),
            build_layout_styles(),
            build_feedback_styles(),
        ]
    )
