from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMenuBar,
    QProgressBar,
    QScrollArea,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QSizePolicy
)

from app.domain.constants import APP_NAME, BASE_DIR, LOGO_PATH, TEMPLATE_PATH
from app.domain.models import AppParams, GenerationResult
from app.domain.validators import ValidationError, validate_app_params
from app.services.export_service import ExportService
from app.services.generation_service import GenerationService
from app.services.template_service import TemplateService
from app.ui.styles import build_stylesheet
from app.ui.widgets.alert_banner import AlertBanner
from app.ui.widgets.header_widget import HeaderWidget
from app.ui.widgets.model_box_widget import ModelBoxWidget
from app.ui.widgets.output_tabs_widget import OutputTabsWidget
from app.ui.widgets.parameters_widget import ParametersWidget
from app.ui.widgets.summary_widget import SummaryWidget
from app.ui.widgets.upload_box_widget import UploadBoxWidget
from app.services.excel_service import ExcelService


class GenerationWorker(QObject):
    """
    Worker executado em thread separada para não travar a interface.
    """

    progress_changed = Signal(int, str)
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, file_path: Path, params: AppParams) -> None:
        super().__init__()
        self.file_path = file_path
        self.params = params

    @Slot()
    def run(self) -> None:
        try:
            self.progress_changed.emit(10, "Validando parâmetros...")
            validate_app_params(self.params)

            self.progress_changed.emit(30, "Lendo planilha...")
            file_bytes = self.file_path.read_bytes()

            self.progress_changed.emit(60, "Gerando arquivos CSV...")
            bundle = GenerationService.build_outputs(file_bytes, self.params)

            self.progress_changed.emit(85, "Compactando arquivos...")
            bundle.zip_bytes = ExportService.build_zip(bundle)

            result = GenerationResult(
                bundle=bundle,
                source_file=self.file_path,
                messages=["Arquivos gerados com sucesso."],
            )

            self.progress_changed.emit(100, "Concluído.")
            self.finished.emit(result)

        except ValidationError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:
            self.failed.emit(f"Erro inesperado: {exc}")


class MainWindow(QMainWindow):
    """Janela principal da aplicação."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(1220, 780)

        if LOGO_PATH.exists():
            self.setWindowIcon(QIcon(str(LOGO_PATH)))

        self.selected_file: Path | None = None
        self.generation_result: GenerationResult | None = None
        self._generation_thread: QThread | None = None
        self._generation_worker: GenerationWorker | None = None

        self._build_ui()
        self.setStyleSheet(build_stylesheet())
        self._connect_actions()
        self._update_generate_state()

    # ========================================================
    # CONSTRUÇÃO DA INTERFACE
    # ========================================================
    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("page")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        # Cabeçalho principal
        root.addWidget(HeaderWidget())

        # Banner de feedback
        self.alert_banner = AlertBanner()
        root.addWidget(self.alert_banner)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("mainProgressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)
        root.addWidget(self.progress_bar)

        # Corpo principal
        content = QHBoxLayout()
        content.setSpacing(16)
        root.addLayout(content, 1)

        content.addWidget(self._build_left_panel(), 5)
        content.addWidget(self._build_right_panel(), 4)

        self.setMenuBar(self._build_menu())
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Pronto.")

    def _build_left_panel(self) -> QScrollArea:
        """
        Painel esquerdo com:
        - modelo oficial
        - upload da planilha
        - parâmetros da importação
        """
        container = QWidget()
        container.setMinimumWidth(0)
        container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.model_box = ModelBoxWidget()
        self.upload_box = UploadBoxWidget()
        self.params_widget = ParametersWidget()

        layout.addWidget(self.model_box)
        layout.addWidget(self.upload_box)
        layout.addWidget(self.params_widget)
        layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setViewportMargins(0, 0, 18, 0)
        scroll.setMinimumWidth(0)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll.setWidget(container)
        return scroll

    def _build_right_panel(self) -> QWidget:
        """
        Painel direito com:
        - resumo da geração
        - visualização dos arquivos
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 16, 0)
        layout.setSpacing(12)

        self.summary_widget = SummaryWidget()
        self.outputs_widget = OutputTabsWidget()

        layout.addWidget(self.summary_widget, 0)
        layout.addWidget(self.outputs_widget, 1)

        return container

    def _build_menu(self) -> QMenuBar:
        """
        Menu superior da aplicação.
        """
        menu = QMenuBar(self)
        arquivo = menu.addMenu("Arquivo")

        actions = [
            ("Selecionar planilha", self.select_excel),
            ("Salvar modelo em outra pasta", self.save_template_copy),
            None,
            ("Salvar CSVs", self.save_csvs),
            ("Salvar ZIP gerado", self.save_zip),
            None,
            ("Sair", self.close),
        ]

        for item in actions:
            if item is None:
                arquivo.addSeparator()
                continue

            text, handler = item
            action = QAction(text, self)
            action.triggered.connect(handler)
            arquivo.addAction(action)

        return menu

    def _connect_actions(self) -> None:
        """
        Conecta eventos da interface aos métodos da janela.
        """
        self.model_box.btn_save_template.clicked.connect(self.save_template_copy)
        self.upload_box.btn_select_excel.clicked.connect(self.select_excel)
        self.upload_box.btn_generate.clicked.connect(self.generate_outputs)
        self.outputs_widget.save_csvs_requested.connect(self.save_csvs)

    # ========================================================
    # FEEDBACK VISUAL / ESTADO DA TELA
    # ========================================================
    def _update_generate_state(self) -> None:
        """
        Habilita ou desabilita o botão de gerar conforme o estado atual.
        """
        can_generate = self.selected_file is not None and self._generation_thread is None
        self.upload_box.btn_generate.setEnabled(can_generate)

    def _show_progress(self, value: int, message: str | None = None) -> None:
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(value)
        if message:
            self.statusBar().showMessage(message)

    def _hide_progress(self) -> None:
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

    def _set_generating_state(self, is_generating: bool) -> None:
        """
        Ajusta o estado visual durante a geração.
        """
        self.upload_box.btn_select_excel.setEnabled(not is_generating)
        self.upload_box.btn_generate.setEnabled(not is_generating)
        self.model_box.btn_save_template.setEnabled(not is_generating)

        if is_generating:
            self.upload_box.btn_generate.setText("Gerando arquivos...")
            self._show_progress(5, "Iniciando processamento...")
        else:
            self.upload_box.btn_generate.setText("Gerar arquivos")
            self._hide_progress()
            self._update_generate_state()

    def _show_success_banner(self, message: str) -> None:
        self.alert_banner.show_message(message, "success")
        self.statusBar().showMessage(message, 5000)

    def _show_error_banner(self, message: str) -> None:
        self.alert_banner.show_message(message, "error", timeout_ms=5000)
        self.statusBar().showMessage("Erro ao processar a operação.", 5000)

    # ========================================================
    # AÇÕES DO USUÁRIO
    # ========================================================
    def select_excel(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar planilha",
            str(BASE_DIR),
            "Excel (*.xlsx)",
        )
        if not file_name:
            return

        selected_file = Path(file_name)

        try:
            credenciadoras = self._extract_credenciadoras_from_file(selected_file)
        except ValidationError as exc:
            self._show_error_banner(str(exc))
            return
        except Exception as exc:
            self._show_error_banner(f"Não foi possível ler as credenciadoras da planilha: {exc}")
            return

        self.selected_file = Path(file_name)
        self.params_widget.set_credenciadoras(credenciadoras)
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
        self._show_success_banner("Modelo salvo com sucesso.")

    def generate_outputs(self) -> None:
        """
        Inicia a geração em thread separada.
        """
        if self.selected_file is None:
            self._show_error_banner("Selecione uma planilha primeiro.")
            return

        params = self.params_widget.get_params()
        try:
            validate_app_params(params)
        except ValidationError as exc:
            self._show_error_banner(str(exc))
            return
        
        self._start_generation_worker(self.selected_file, params)

    def save_csvs(self) -> None:
        if self.generation_result is None:
            self._show_error_banner("Gere os arquivos antes de salvar os CSVs.")
            return

        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta para salvar os CSVs",
        )
        if not folder:
            return

        ExportService.save_csvs(self.generation_result.bundle, Path(folder))
        self._show_success_banner("CSVs salvos com sucesso.")

    def save_zip(self) -> None:
        if self.generation_result is None or self.generation_result.bundle.zip_bytes is None:
            self._show_error_banner("Gere os arquivos antes de salvar o ZIP.")
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
        self._show_success_banner("ZIP salvo com sucesso.")

    # ========================================================
    # GERAÇÃO EM THREAD
    # ========================================================
    def _start_generation_worker(self, file_path: Path, params: AppParams) -> None:
        """
        Cria e inicia a thread de geração.
        """
        self._set_generating_state(True)

        self._generation_thread = QThread(self)
        self._generation_worker = GenerationWorker(file_path, params)
        self._generation_worker.moveToThread(self._generation_thread)

        self._generation_thread.started.connect(self._generation_worker.run)
        self._generation_worker.progress_changed.connect(self._on_generation_progress)
        self._generation_worker.finished.connect(self._on_generation_finished)
        self._generation_worker.failed.connect(self._on_generation_failed)

        self._generation_worker.finished.connect(self._generation_thread.quit)
        self._generation_worker.failed.connect(self._generation_thread.quit)

        self._generation_thread.finished.connect(self._generation_thread.deleteLater)
        self._generation_thread.finished.connect(self._cleanup_generation_worker)

        self._generation_thread.start()

    @Slot(int, str)
    def _on_generation_progress(self, value: int, message: str) -> None:
        self._show_progress(value, message)

    @Slot(object)
    def _on_generation_finished(self, result: object) -> None:
        """
        Finaliza a geração com sucesso.
        """
        self.generation_result = result  # type: ignore[assignment]

        self.summary_widget.update_counts(self.generation_result.bundle.counts())
        self.outputs_widget.populate(self.generation_result.bundle.tables)

        self._set_generating_state(False)
        self._show_success_banner("Arquivos gerados com sucesso.")

    @Slot(str)
    def _on_generation_failed(self, message: str) -> None:
        """
        Finaliza a geração com erro.
        """
        self._set_generating_state(False)
        self._show_error_banner(message)

    @Slot()
    def _cleanup_generation_worker(self) -> None:
        """
        Limpa referências da thread/worker após finalização.
        """
        self._generation_worker = None
        self._generation_thread = None
        self._update_generate_state()

    def _extract_credenciadoras_from_file(self, file_path: Path) -> list[str]:
        file_bytes = file_path.read_bytes()
        taxas_df = ExcelService.read_taxas(file_bytes)

        if "CREDENCIADORA" not in taxas_df.columns:
            raise ValidationError("A coluna CREDENCIADORA não foi encontrada na aba TAXAS.")

        credenciadoras = (
            taxas_df["CREDENCIADORA"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        return credenciadoras