from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout

from app.ui.widgets.section_header import SectionHeader


class MetricCard(QFrame):

    def __init__(self, title: str, object_name: str) -> None:
        super().__init__()
        self.setObjectName(object_name)
        self.setProperty("class", "metricCard")
        self.setMinimumHeight(108)
        self.setMaximumHeight(124)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(8)

        self.value_label = QLabel("0")
        self.value_label.setObjectName("metricValue")
        self.value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("metricLabel")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        root.addWidget(self.value_label)
        root.addWidget(self.title_label)
        root.addStretch()

    def set_value(self, value: int) -> None:
        self.value_label.setText(str(value))


class SummaryWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 18, 14, 14)
        root.setSpacing(12)

        root.addWidget(SectionHeader("Resumo da geração"))

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        self.card_portadores = MetricCard("Portadores", "metricCardBlue")
        self.card_cartoes = MetricCard("Cartões", "metricCardGreen")
        self.card_prazos = MetricCard("Prazos", "metricCardYellow")
        self.card_retencoes = MetricCard("Retenções", "metricCardPurple")

        row.addWidget(self.card_portadores, 1)
        row.addWidget(self.card_cartoes, 1)
        row.addWidget(self.card_prazos, 1)
        row.addWidget(self.card_retencoes, 1)

        root.addLayout(row)

    def update_counts(self, counts: dict[str, int]) -> None:
        self.card_portadores.set_value(counts.get("portadores", counts.get("portadores.csv", 0)))
        self.card_cartoes.set_value(counts.get("cartoes", counts.get("cartoes.csv", 0)))
        self.card_prazos.set_value(counts.get("prazos", counts.get("prazos.csv", 0)))
        self.card_retencoes.set_value(counts.get("retencoes", counts.get("retencoes.csv", 0)))