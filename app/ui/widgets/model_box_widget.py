from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from app.ui.widgets.section_header import SectionHeader

class ModelBoxWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.addWidget(SectionHeader( "Modelo oficial"))

        info = QLabel(
            "Use sempre o modelo oficial. Ele já considera taxas por empresa, dias por tipo e parcelas de 1x a 24x."
        )
        info.setWordWrap(True)
        info.setObjectName("mutedText")
        layout.addWidget(info)

        row = QHBoxLayout()
        row.setSpacing(10)

        self.btn_save_template = QPushButton("Salvar modelo Excel")
        self.btn_save_template.setObjectName("successButton")

        row.addWidget(self.btn_save_template)

        layout.addLayout(row)