from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QGridLayout, QLabel, QSpinBox

from app.ui.widgets.custom_combo import CustomComboBox

def create_form_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("formLabel")
    return label


def create_help_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("fieldHelp")
    label.setWordWrap(True)
    return label


def add_labeled_widget(
    grid: QGridLayout,
    row: int,
    col: int,
    label_text: str,
    widget,
) -> None:
    grid.addWidget(create_form_label(label_text), row, col)
    grid.addWidget(widget, row, col + 1)


def create_combo_from_options(
    options: list[tuple[str, str]],
    current_value: str,
) -> QComboBox:
    combo = CustomComboBox()
    for label, value in options:
        combo.addItem(label, value)

    index = combo.findData(current_value)
    if index >= 0:
        combo.setCurrentIndex(index)

    return combo


def create_spinbox(
    minimum: int,
    maximum: int,
    value: int,
) -> QSpinBox:
    spin = QSpinBox()
    spin.setRange(minimum, maximum)
    spin.setValue(value)
    return spin


def create_checkbox(text: str, checked: bool = False) -> QCheckBox:
    checkbox = QCheckBox(text)
    checkbox.setChecked(checked)
    return checkbox