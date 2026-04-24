from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout


class AlertBanner(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("alertBanner")
        self.setVisible(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)

        self.label = QLabel("")
        self.label.setObjectName("alertText")
        layout.addWidget(self.label)

    def show_message(self, message: str, type_: str = "success", timeout_ms: int = 4000) -> None:
        self.setObjectName(f"alertBanner_{type_}")
        self.style().unpolish(self)
        self.style().polish(self)

        self.label.setText(message)
        self.setVisible(True)

        if timeout_ms > 0:
            QTimer.singleShot(timeout_ms, self.hide)