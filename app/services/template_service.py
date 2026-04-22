from __future__ import annotations

from pathlib import Path
import shutil

from app.domain.constants import TEMPLATE_PATH


class TemplateService:
    @staticmethod
    def save_copy(destination: Path) -> Path:
        shutil.copy2(TEMPLATE_PATH, destination)
        return destination
