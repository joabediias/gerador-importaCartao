from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class ModelBoxWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("1. Modelo oficial")
        layout = QVBoxLayout(self)

        info = QLabel(
            "Use sempre o modelo oficial. Ele já considera taxas por empresa, dias por tipo e parcelas de 1x a 24x."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        row = QHBoxLayout()
        self.btn_save_template = QPushButton("Salvar modelo Excel")
        self.btn_open_folder = QPushButton("Abrir pasta da aplicação")
        row.addWidget(self.btn_save_template)
        row.addWidget(self.btn_open_folder)
        layout.addLayout(row)
