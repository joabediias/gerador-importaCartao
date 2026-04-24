from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from app.domain.constants import APP_NAME, APP_VERSION, ICON_APP_CARD
from app.ui.svg_icon import svg_to_pixmap


class HeaderWidget(QFrame):
    """Cabeçalho principal da aplicação."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("headerCard")
        self._build_ui()

    def _build_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(22, 18, 22, 18)
        root.setSpacing(18)

        # Bloco esquerdo: ícone + textos
        left_wrap = QHBoxLayout()
        left_wrap.setSpacing(16)

        icon_box = QFrame()
        icon_box.setObjectName("headerIconBox")
        icon_box.setFixedSize(74, 74)

        icon_layout = QVBoxLayout(icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel()
        icon_label.setObjectName("headerIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setPixmap(svg_to_pixmap(ICON_APP_CARD, 34))
        icon_layout.addWidget(icon_label)

        left_wrap.addWidget(icon_box)

        text_wrap = QVBoxLayout()
        text_wrap.setSpacing(4)

        title = QLabel(APP_NAME)
        title.setObjectName("heroTitle")

        subtitle = QLabel("Gerador local de arquivos CSV para importação de cartões")
        subtitle.setObjectName("heroSubtitle")

        helper = QLabel("Planilha padrão + parâmetros na aplicação + geração dos 4 CSVs")
        helper.setObjectName("heroHelper")

        text_wrap.addWidget(title)
        text_wrap.addWidget(subtitle)
        text_wrap.addSpacing(6)
        text_wrap.addWidget(helper)

        left_wrap.addLayout(text_wrap, 1)

        left_widget = QWidget()
        left_widget.setObjectName("headerLeftWidget")
        left_widget.setLayout(left_wrap)
        left_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        root.addWidget(left_widget, 1)

        # Bloco direito: versão
        version_box = QFrame()
        version_box.setObjectName("headerVersionBox")
        version_box.setFixedWidth(130)

        version_layout = QVBoxLayout(version_box)
        version_layout.setContentsMargins(10, 12, 10, 12)
        version_layout.setSpacing(8)

        version_title = QLabel(f"Versão {APP_VERSION}")
        version_title.setObjectName("headerVersionTitle")
        version_title.setAlignment(Qt.AlignCenter)

        version_sub = QLabel("Layout Cartao")
        version_sub.setObjectName("headerVersionSub")
        version_sub.setAlignment(Qt.AlignCenter)

        version_layout.addStretch()
        version_layout.addWidget(version_title)
        version_layout.addWidget(version_sub)
        version_layout.addStretch()

        root.addWidget(version_box)
