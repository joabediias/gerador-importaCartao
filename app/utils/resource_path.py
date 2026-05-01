from __future__ import annotations

import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto do recurso no modo normal,
    no PyInstaller --onedir e no PyInstaller --onefile.
    """
    if getattr(sys, "frozen", False):
        # PyInstaller --onefile
        if hasattr(sys, "_MEIPASS"):
            base_path = Path(sys._MEIPASS)
        else:
            # PyInstaller --onedir
            base_path = Path(sys.executable).parent / "_internal"
    else:
        # desenvolvimento
        base_path = Path.cwd()

    return (base_path / relative_path).as_posix()