from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ComboPopup(QFrame):
    item_selected = Signal(str, object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setObjectName("customComboPopup")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("customComboList")
        self.list_widget.setFrameShape(QFrame.NoFrame)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.itemClicked.connect(self._on_item_clicked)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(self.list_widget)

    def set_items(self, items: list[tuple[str, object]]) -> None:
        self.list_widget.clear()
        for label, value in items:
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, value)
            self.list_widget.addItem(item)

    def select_by_value(self, value: object) -> None:
        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            if item.data(Qt.UserRole) == value:
                self.list_widget.setCurrentRow(row)
                return

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        self.item_selected.emit(item.text(), item.data(Qt.UserRole))
        self.hide()

class CustomComboBox(QWidget):
    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._items: list[tuple[str, object]] = []
        self._current_index = -1

        self.setObjectName("customCombo")

        self.display = QPushButton("")
        self.display.setObjectName("customComboDisplay")
        self.display.setCursor(Qt.PointingHandCursor)
        self.display.clicked.connect(self._toggle_popup)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.addWidget(self.display)

        self.popup = ComboPopup(self)
        self.popup.item_selected.connect(self._on_popup_selected)

    def addItem(self, label: str, value: object = None) -> None:
        self._items.append((label, value))
        if self._current_index == -1:
            self.setCurrentIndex(0)

    def findData(self, value: object) -> int:
        for i, (_, item_value) in enumerate(self._items):
            if item_value == value:
                return i
        return -1

    def setCurrentIndex(self, index: int) -> None:
        if 0 <= index < len(self._items):
            self._current_index = index
            label, _ = self._items[index]
            self.display.setText(label)
            self.currentIndexChanged.emit(index)
            self.currentTextChanged.emit(label)

    def currentIndex(self) -> int:
        return self._current_index

    def currentText(self) -> str:
        if 0 <= self._current_index < len(self._items):
            return self._items[self._current_index][0]
        return ""

    def currentData(self):
        if 0 <= self._current_index < len(self._items):
            return self._items[self._current_index][1]
        return None

    def _toggle_popup(self) -> None:
        if self.popup.isVisible():
            self.popup.hide()
            return

        self.popup.set_items(self._items)
        self.popup.select_by_value(self.currentData())
        self.popup.setFixedWidth(self.width())

        row_height = max(34, self.popup.list_widget.sizeHintForRow(0))
        popup_height = min(220, row_height * max(1, len(self._items)) + 12)
        self.popup.resize(self.width(), popup_height)

        pos = self.mapToGlobal(QPoint(0, self.height() + 4))
        self.popup.move(pos)
        self.popup.show()

    def _on_popup_selected(self, label: str, value: object) -> None:
        index = self.findData(value)
        if index >= 0:
            self.setCurrentIndex(index)