from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.domain.constants import APP_NAME, APP_SUBTITLE, LOGO_PATH


class HeaderWidget(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("headerCard")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(16)

        logo = QLabel()
        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH)).scaled(76, 76, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            logo.setFixedSize(84, 84)
            logo.setAlignment(Qt.AlignCenter)
        else:
            logo.setText("💳")
        layout.addWidget(logo, 0, Qt.AlignTop)

        texts = QVBoxLayout()
        title = QLabel(APP_NAME)
        title.setObjectName("heroTitle")
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setObjectName("heroSubtitle")
        helper = QLabel("Planilha padrão + parâmetros na aplicação + geração dos 4 CSVs")
        helper.setObjectName("heroHelper")
        texts.addWidget(title)
        texts.addWidget(subtitle)
        texts.addWidget(helper)
        layout.addLayout(texts, 1)

        right = QVBoxLayout()
        status = QLabel("Versão 1.0.3")
        status.setObjectName("statusPill")
        right.addWidget(status)
        layout.addLayout(right)
