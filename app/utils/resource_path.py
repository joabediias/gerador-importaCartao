from __future__ import annotations

import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto de um recurso tanto no modo dev
    quanto no executável gerado pelo PyInstaller --onedir.
    """
    if getattr(sys, "frozen", False):
        base_path = Path(sys.executable).parent / "_internal"
    else:
        base_path = Path.cwd()

    return (base_path / relative_path).as_posix()