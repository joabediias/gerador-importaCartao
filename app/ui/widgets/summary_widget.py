from PySide6.QtWidgets import QGridLayout, QGroupBox, QLabel, QVBoxLayout, QWidget


class SummaryWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("4. Resumo da geração")
        layout = QGridLayout(self)
        self.metrics = {}
        labels = [
            ("portadores.csv", "Portadores"),
            ("cartoes.csv", "Cartões"),
            ("prazos.csv", "Prazos"),
            ("retencoes.csv", "Retenções"),
        ]
        for idx, (key, title) in enumerate(labels):
            card = QWidget()
            card_layout = QVBoxLayout(card)
            value = QLabel("0")
            value.setObjectName("metricValue")
            label = QLabel(title)
            label.setObjectName("metricLabel")
            card_layout.addWidget(value)
            card_layout.addWidget(label)
            layout.addWidget(card, idx // 2, idx % 2)
            self.metrics[key] = value

    def update_counts(self, counts: dict[str, int]) -> None:
        for key, widget in self.metrics.items():
            widget.setText(str(counts.get(key, 0)))
