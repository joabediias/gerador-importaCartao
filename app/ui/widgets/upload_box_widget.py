from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from app.ui.widgets.section_header import SectionHeader

class UploadBoxWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.addWidget(SectionHeader("Planilha preenchida"))

        self.lbl_selected_file = QLabel("Nenhuma planilha selecionada.")
        self.lbl_selected_file.setObjectName("mutedText")
        self.lbl_selected_file.setWordWrap(True)
        layout.addWidget(self.lbl_selected_file)

        row = QHBoxLayout()
        self.btn_select_excel = QPushButton("Selecionar planilha")
        self.btn_select_excel.setObjectName("ghostButton")

        self.btn_generate = QPushButton("Gerar arquivos")
        self.btn_generate.setObjectName("primaryButton")
        
        row.addWidget(self.btn_select_excel)
        row.addWidget(self.btn_generate)
        layout.addLayout(row)
