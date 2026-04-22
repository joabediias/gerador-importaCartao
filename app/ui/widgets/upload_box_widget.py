from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class UploadBoxWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("2. Planilha preenchida")
        layout = QVBoxLayout(self)

        self.lbl_selected_file = QLabel("Nenhuma planilha selecionada.")
        self.lbl_selected_file.setObjectName("mutedText")
        self.lbl_selected_file.setWordWrap(True)
        layout.addWidget(self.lbl_selected_file)

        row = QHBoxLayout()
        self.btn_select_excel = QPushButton("Selecionar planilha")
        self.btn_generate = QPushButton("Gerar arquivos")
        self.btn_generate.setObjectName("primaryButton")
        row.addWidget(self.btn_select_excel)
        row.addWidget(self.btn_generate)
        layout.addLayout(row)
