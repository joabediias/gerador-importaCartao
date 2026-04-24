from __future__ import annotations

import pandas as pd
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.ui.widgets.section_header import SectionHeader


class OutputTabsWidget(QGroupBox):
    """Exibe a pré-visualização tabulada dos CSVs gerados."""

    save_csvs_requested = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(14, 18, 14, 14)
        self.layout.setSpacing(16)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)
        header_row.addWidget(SectionHeader("Visualização dos arquivos"), 1)

        self.btn_save_csvs = QPushButton("Salvar CSVs")
        self.btn_save_csvs.setObjectName("successButton")
        self.btn_save_csvs.clicked.connect(self.save_csvs_requested.emit)
        self.btn_save_csvs.setEnabled(False)
        
        header_row.addWidget(self.btn_save_csvs, 0, Qt.AlignRight)

        self.layout.addLayout(header_row)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.show_empty_state()

    def show_empty_state(self) -> None:
        self.tabs.clear()
        self.btn_save_csvs.setEnabled(False)

        empty_page = QWidget()
        empty_layout = QVBoxLayout(empty_page)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_layout.setSpacing(10)

        icon = QLabel("📦")
        icon.setAlignment(Qt.AlignCenter)
        icon.setObjectName("emptyIcon")

        title = QLabel("Nenhum arquivo gerado ainda")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("emptyTitle")

        subtitle = QLabel('Preencha os parâmetros e clique em "Gerar arquivos"')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("emptySubtitle")

        empty_layout.addWidget(icon)
        empty_layout.addWidget(title)
        empty_layout.addWidget(subtitle)

        self.tabs.addTab(empty_page, "Aguardando geração")

    def populate(self, outputs: dict[str, pd.DataFrame]) -> None:
        self.tabs.clear()

        if not outputs:
            self.show_empty_state()
            return

        self.btn_save_csvs.setEnabled(True)

        for filename, df in outputs.items():
            table = QTableWidget()
            table.setColumnCount(len(df.columns))
            table.setHorizontalHeaderLabels([str(c) for c in df.columns])
            table.setRowCount(min(len(df), 200))

            for row_idx in range(min(len(df), 200)):
                for col_idx, col_name in enumerate(df.columns):
                    value = "" if pd.isna(df.iloc[row_idx, col_idx]) else str(df.iloc[row_idx, col_idx])
                    table.setItem(row_idx, col_idx, QTableWidgetItem(value))

            table.resizeColumnsToContents()
            self.tabs.addTab(table, filename)
