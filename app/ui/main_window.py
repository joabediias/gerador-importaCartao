from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QStatusBar,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.domain.constants import APP_NAME, BASE_DIR, LOGO_PATH, TEMPLATE_PATH
from app.domain.validators import ValidationError, validate_app_params
from app.services.export_service import ExportService
from app.services.template_service import TemplateService
from app.ui.styles import build_stylesheet
from app.ui.widgets.header_widget import HeaderWidget
from app.ui.widgets.model_box_widget import ModelBoxWidget
from app.ui.widgets.output_tabs_widget import OutputTabsWidget
from app.ui.widgets.parameters_widget import ParametersWidget
from app.ui.widgets.summary_widget import SummaryWidget
from app.ui.widgets.upload_box_widget import UploadBoxWidget
from app.use_cases.generate_files import generate_import_files


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(1220, 780)
        if LOGO_PATH.exists():
            self.setWindowIcon(QIcon(str(LOGO_PATH)))

        self.selected_file: Path | None = None
        self.generation_result = None

        self._build_ui()
        self.setStyleSheet(build_stylesheet())
        self._connect_actions()
        self._update_generate_state()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("page")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        root.addWidget(HeaderWidget())

        content = QHBoxLayout()
        content.setSpacing(16)
        root.addLayout(content, 1)

        # ===== Coluna esquerda =====
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        self.model_box = ModelBoxWidget()
        self.upload_box = UploadBoxWidget()
        self.params_widget = ParametersWidget()

        left_layout.addWidget(self.model_box)
        left_layout.addWidget(self.upload_box)
        left_layout.addWidget(self.params_widget)
        left_layout.addStretch(1)

        self.left_scroll = QScrollArea()
        self.left_scroll.setWidgetResizable(True)
        self.left_scroll.setFrameShape(QScrollArea.NoFrame)
        self.left_scroll.setWidget(left_container)

        # ===== Coluna direita =====
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        self.summary_widget = SummaryWidget()
        self.outputs_widget = OutputTabsWidget()

        right_layout.addWidget(self.summary_widget)
        right_layout.addWidget(self.outputs_widget, 1)

        # Proporção das colunas
        content.addWidget(self.left_scroll, 5)
        content.addWidget(right_container, 4)

        self.setMenuBar(self._build_menu())
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Pronto.")

    def _build_menu(self) -> QMenuBar:
        menu = QMenuBar(self)
        arquivo = menu.addMenu("Arquivo")

        abrir_action = QAction("Selecionar planilha", self)
        abrir_action.triggered.connect(self.select_excel)
        arquivo.addAction(abrir_action)

        baixar_modelo_action = QAction("Salvar modelo em outra pasta", self)
        baixar_modelo_action.triggered.connect(self.save_template_copy)
        arquivo.addAction(baixar_modelo_action)

        arquivo.addSeparator()
        salvar_csv_action = QAction("Salvar CSVs", self)
        salvar_csv_action.triggered.connect(self.save_csvs)
        arquivo.addAction(salvar_csv_action)

        salvar_zip_action = QAction("Salvar ZIP gerado", self)
        salvar_zip_action.triggered.connect(self.save_zip)
        arquivo.addAction(salvar_zip_action)

        arquivo.addSeparator()
        sair_action = QAction("Sair", self)
        sair_action.triggered.connect(self.close)
        arquivo.addAction(sair_action)

        ajuda = menu.addMenu("Ajuda")
        abrir_pasta_action = QAction("Abrir pasta da aplicação", self)
        abrir_pasta_action.triggered.connect(self.open_app_folder)
        ajuda.addAction(abrir_pasta_action)

        return menu

    def _connect_actions(self) -> None:
        self.model_box.btn_save_template.clicked.connect(self.save_template_copy)
        self.model_box.btn_open_folder.clicked.connect(self.open_app_folder)
        self.upload_box.btn_select_excel.clicked.connect(self.select_excel)
        self.upload_box.btn_generate.clicked.connect(self.generate_outputs)

    def _update_generate_state(self) -> None:
        self.upload_box.btn_generate.setEnabled(self.selected_file is not None)

    def select_excel(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar planilha",
            str(BASE_DIR),
            "Excel (*.xlsx)",
        )
        if not file_name:
            return
        self.selected_file = Path(file_name)
        self.upload_box.lbl_selected_file.setText(str(self.selected_file))
        self.statusBar().showMessage("Planilha selecionada.")
        self._update_generate_state()

    def save_template_copy(self) -> None:
        target, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar modelo",
            str(TEMPLATE_PATH.name),
            "Excel (*.xlsx)",
        )
        if not target:
            return
        TemplateService.save_copy(Path(target))
        self.statusBar().showMessage("Modelo salvo com sucesso.")
        QMessageBox.information(self, APP_NAME, "Modelo salvo com sucesso.")

    def open_app_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(BASE_DIR)))

    def generate_outputs(self) -> None:
        if self.selected_file is None:
            QMessageBox.warning(self, APP_NAME, "Selecione uma planilha primeiro.")
            return
        params = self.params_widget.get_params()
        try:
            validate_app_params(params)
            result = generate_import_files(self.selected_file, params)
        except ValidationError as exc:
            QMessageBox.critical(self, APP_NAME, str(exc))
            self.statusBar().showMessage("Erro de validação.")
            return
        except Exception as exc:
            QMessageBox.critical(self, APP_NAME, f"Erro inesperado: {exc}")
            self.statusBar().showMessage("Erro inesperado.")
            return

        self.generation_result = result
        self.summary_widget.update_counts(result.bundle.counts())
        self.outputs_widget.populate(result.bundle.tables)
        self.statusBar().showMessage("Arquivos gerados com sucesso.")
        QMessageBox.information(self, APP_NAME, "Arquivos gerados com sucesso.")

    def save_csvs(self) -> None:
        if self.generation_result is None:
            QMessageBox.warning(self, APP_NAME, "Gere os arquivos antes de salvar.")
            return
        folder = QFileDialog.getExistingDirectory(self, "Selecionar pasta para salvar os CSVs")
        if not folder:
            return
        ExportService.save_csvs(self.generation_result.bundle, Path(folder))
        QMessageBox.information(self, APP_NAME, "CSVs salvos com sucesso.")

    def save_zip(self) -> None:
        if self.generation_result is None or self.generation_result.bundle.zip_bytes is None:
            QMessageBox.warning(self, APP_NAME, "Gere os arquivos antes de salvar o ZIP.")
            return
        target, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar ZIP",
            "layout_importacartao_saida.zip",
            "ZIP (*.zip)",
        )
        if not target:
            return
        ExportService.save_zip_file(self.generation_result.bundle.zip_bytes, Path(target))
        QMessageBox.information(self, APP_NAME, "ZIP salvo com sucesso.")
