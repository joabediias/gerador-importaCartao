from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.ui.styles import configure_application


def run_app() -> None:
    app = QApplication(sys.argv)
    configure_application(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
