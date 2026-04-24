from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class SectionHeader(QWidget):
    def __init__(self, icon_or_title: str | Path, title: str | None = None):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.title = QLabel()
        self.title.setObjectName("sectionTitle")
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        if title is None:
            self.title.setText(str(icon_or_title))
            layout.addWidget(self.title)
            layout.addStretch()
            return

        self.title.setText(title)
        layout.addWidget(self.title)
        layout.addStretch()