from __future__ import annotations

import pandas as pd
from PySide6.QtWidgets import QGroupBox, QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


class OutputTabsWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("5. Visualização dos arquivos")
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

    def populate(self, outputs: dict[str, pd.DataFrame]) -> None:
        self.tabs.clear()
        for filename, df in outputs.items():
            table = QTableWidget()
            table.setColumnCount(len(df.columns))
            table.setHorizontalHeaderLabels([str(c) for c in df.columns])
            table.setRowCount(min(len(df), 200))
            for r in range(min(len(df), 200)):
                for c, col in enumerate(df.columns):
                    value = "" if pd.isna(df.iloc[r, c]) else str(df.iloc[r, c])
                    table.setItem(r, c, QTableWidgetItem(value))
            table.resizeColumnsToContents()
            self.tabs.addTab(table, filename)
