from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Dict

import pandas as pd
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QColor, QDesktopServices, QIcon, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStatusBar,
    QStyleFactory,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core import AppParams, ValidationError, build_outputs, build_zip


APP_NAME = "Layout ImportaCartão"
APP_SUBTITLE = "Gerador local de arquivos CSV para importação de cartões"
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATE_PATH = BASE_DIR / "modelo_taxas_cartao_melhorado.xlsx"
LOGO_PATH = ASSETS_DIR / "logo_importacartao.png"
BANNER_PATH = ASSETS_DIR / "banner_importacartao.png"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(1220, 780)

        if LOGO_PATH.exists():
            self.setWindowIcon(QIcon(str(LOGO_PATH)))

        self.selected_file: Path | None = None
        self.outputs: Dict[str, pd.DataFrame] = {}
        self.last_zip_bytes: bytes | None = None

        self._build_ui()
        self._apply_styles()
        self._connect_actions()
        self._update_generate_state()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        root.addWidget(self._build_header())

        content = QHBoxLayout()
        content.setSpacing(16)
        root.addLayout(content, 1)

        left_panel = QVBoxLayout()
        left_panel.setSpacing(12)
        left_panel.setContentsMargins(0, 0, 0, 0)
        content.addLayout(left_panel, 0)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(12)
        right_panel.setContentsMargins(0, 0, 0, 0)
        content.addLayout(right_panel, 1)

        left_panel.addWidget(self._build_model_box())
        left_panel.addWidget(self._build_upload_box())
        left_panel.addWidget(self._build_params_box())
        left_panel.addStretch(1)

        right_panel.addWidget(self._build_summary_box())
        right_panel.addWidget(self._build_output_box(), 1)

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

    def _build_header(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("headerCard")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(16)

        logo = QLabel()
        logo.setObjectName("logoBadge")
        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH)).scaled(76, 76, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
            logo.setFixedSize(84, 84)
            logo.setAlignment(Qt.AlignCenter)
        else:
            logo.setText("💳")
            logo.setObjectName("heroIcon")
        layout.addWidget(logo, 0, Qt.AlignTop)

        texts = QVBoxLayout()
        texts.setSpacing(4)
        title = QLabel(APP_NAME)
        title.setObjectName("heroTitle")
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setObjectName("heroSubtitle")
        helper = QLabel("Planilha padrão + parâmetros na aplicação + geração dos 4 CSVs")
        helper.setObjectName("heroHelper")
        texts.addWidget(title)
        texts.addWidget(subtitle)
        texts.addWidget(helper)
        layout.addLayout(texts, 1)

        badge_wrap = QVBoxLayout()
        badge_wrap.setSpacing(8)
        badge_wrap.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        badge = QLabel("Desktop • PySide6")
        badge.setObjectName("badge")
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedHeight(34)
        badge.setMinimumWidth(146)

        status = QLabel("Visual v3")
        status.setObjectName("statusPill")
        status.setAlignment(Qt.AlignCenter)
        status.setFixedHeight(30)

        badge_wrap.addWidget(badge)
        badge_wrap.addWidget(status)
        layout.addLayout(badge_wrap)
        return frame

    def _build_model_box(self) -> QWidget:
        box = self._section_box("1. Modelo oficial")
        layout = box.layout()

        info = QLabel(
            "Use sempre o modelo oficial. Ele já considera taxas por empresa, dias por tipo e parcelas de 1x a 24x."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        buttons = QHBoxLayout()
        self.btn_save_template = QPushButton("Salvar modelo Excel")
        self.btn_open_template_folder = QPushButton("Abrir pasta da aplicação")
        buttons.addWidget(self.btn_save_template)
        buttons.addWidget(self.btn_open_template_folder)
        layout.addLayout(buttons)
        return box

    def _build_upload_box(self) -> QWidget:
        box = self._section_box("2. Planilha preenchida")
        layout = box.layout()

        self.lbl_selected_file = QLabel("Nenhuma planilha selecionada.")
        self.lbl_selected_file.setObjectName("mutedText")
        self.lbl_selected_file.setWordWrap(True)
        layout.addWidget(self.lbl_selected_file)

        row = QHBoxLayout()
        self.btn_select_excel = QPushButton("Selecionar planilha")
        self.btn_generate = QPushButton("Gerar arquivos")
        self.btn_generate.setObjectName("primaryButton")
        row.addWidget(self.btn_select_excel)
        row.addWidget(self.btn_generate)
        layout.addLayout(row)
        return box

    def _build_params_box(self) -> QWidget:
        box = self._section_box("3. Parâmetros da importação")
        main = box.layout()

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(10)

        self.cmb_tipo_recebimento = self._combo(["POS", "TEF", "AMBOS"], "POS")
        self.cmb_liberada = self._combo(["S", "N"], "S")
        self.spn_credenciadora_id = QSpinBox()
        self.spn_credenciadora_id.setRange(1, 999999)
        self.spn_credenciadora_id.setValue(42)
        self.cmb_vendas_web = self._combo(["S", "N"], "S")
        self.cmb_forma_calc = self._combo(["A", "T"], "A")
        self.cmb_perm_vincular = self._combo(["S", "N"], "S")
        self.cmb_tipo_venc_parcelas = self._combo(["F", "U"], "U")
        self.cmb_tipo_parcelamento = self._combo(["L", "O"], "L")
        self.cmb_dia_inicio = self._combo(["V", "D"], "V")
        self.cmb_dias_primeira = self._combo(["M", "D"], "M")
        self.cmb_tipo_cobranca = self._combo(["P", "A"], "P")
        self.cmb_venc_prox_util = self._combo(["S", "N"], "S")
        self.chk_receb_unico = QCheckBox("Recebimento único PagSeguro")
        self.chk_apenas_uteis = QCheckBox("Apenas dias úteis no cálculo do prazo")
        self.cmb_tipo_inicio_periodo = self._combo(["V", "D"], "V")
        self.cmb_tipo_venc_primeira = self._combo(["M", "D"], "M")

        fields = [
            ("Tipo de recebimento", self.cmb_tipo_recebimento),
            ("Liberada cons. final padrão", self.cmb_liberada),
            ("Credenciadora ID", self.spn_credenciadora_id),
            ("Utilizar em vendas web", self.cmb_vendas_web),
            ("Forma calc. diferença cartão parc.", self.cmb_forma_calc),
            ("Permitir vincular cartão aut. caixa", self.cmb_perm_vincular),
            ("Tipo vencimento parcelas", self.cmb_tipo_venc_parcelas),
            ("Tipo parcelamento", self.cmb_tipo_parcelamento),
            ("Dia início período vencimento", self.cmb_dia_inicio),
            ("Dias p/ venc. primeira parcela", self.cmb_dias_primeira),
            ("Tipo cobrança retenção", self.cmb_tipo_cobranca),
            ("Vencimento parc. próximo dia útil", self.cmb_venc_prox_util),
            ("Tipo início período vencimento", self.cmb_tipo_inicio_periodo),
            ("Tipo vencimento primeira parcela", self.cmb_tipo_venc_primeira),
        ]

        for idx, (label, widget) in enumerate(fields):
            r = idx // 2
            c = (idx % 2) * 2
            label_widget = QLabel(label)
            label_widget.setObjectName("fieldLabel")
            grid.addWidget(label_widget, r, c)
            grid.addWidget(widget, r, c + 1)

        main.addLayout(grid)
        main.addWidget(self.chk_receb_unico)
        main.addWidget(self.chk_apenas_uteis)
        return box

    def _build_summary_box(self) -> QWidget:
        box = self._section_box("Resumo da geração")
        layout = box.layout()

        metrics = QGridLayout()
        metrics.setHorizontalSpacing(12)
        metrics.setVerticalSpacing(12)

        self.metric_portadores = self._metric_card("Portadores", "0")
        self.metric_cartoes = self._metric_card("Cartões", "0")
        self.metric_prazos = self._metric_card("Prazos", "0")
        self.metric_retencoes = self._metric_card("Retenções", "0")

        metric_widgets = [
            self.metric_portadores,
            self.metric_cartoes,
            self.metric_prazos,
            self.metric_retencoes,
        ]
        for idx, widget in enumerate(metric_widgets):
            metrics.addWidget(widget, 0, idx)

        layout.addLayout(metrics)

        actions = QHBoxLayout()
        self.btn_save_zip = QPushButton("Salvar ZIP")
        self.btn_export_folder = QPushButton("Salvar CSVs em pasta")
        actions.addWidget(self.btn_save_zip)
        actions.addWidget(self.btn_export_folder)
        layout.addLayout(actions)

        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setPlaceholderText("Mensagens e validações aparecerão aqui.")
        self.txt_log.setFixedHeight(126)
        layout.addWidget(self.txt_log)
        return box

    def _build_output_box(self) -> QWidget:
        box = self._section_box("Pré-visualização dos arquivos")
        layout = box.layout()

        self.tabs = QTabWidget()
        self.tables: dict[str, QTableWidget] = {}
        for name in ["portadores.csv", "cartoes.csv", "prazos.csv", "retencoes.csv"]:
            table = QTableWidget()
            table.setAlternatingRowColors(True)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            table.setSelectionMode(QTableWidget.SingleSelection)
            table.setSortingEnabled(False)
            table.verticalHeader().setVisible(False)
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.tables[name] = table
            self.tabs.addTab(table, name)

        layout.addWidget(self.tabs)
        return box

    def _section_box(self, title: str) -> QGroupBox:
        box = QGroupBox(title)
        layout = QVBoxLayout(box)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        return box

    def _metric_card(self, title: str, value: str) -> QWidget:
        card = QFrame()
        card.setObjectName("metricCard")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(4)
        label_title = QLabel(title)
        label_title.setObjectName("metricTitle")
        label_value = QLabel(value)
        label_value.setObjectName("metricValue")
        label_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lay.addWidget(label_title)
        lay.addWidget(label_value)
        card.metric_value = label_value  # type: ignore[attr-defined]
        return card

    def _combo(self, items: list[str], default: str) -> QComboBox:
        combo = QComboBox()
        combo.addItems(items)
        combo.setCurrentText(default)
        return combo

    def _connect_actions(self) -> None:
        self.btn_save_template.clicked.connect(self.save_template_copy)
        self.btn_open_template_folder.clicked.connect(self.open_app_folder)
        self.btn_select_excel.clicked.connect(self.select_excel)
        self.btn_generate.clicked.connect(self.generate_outputs)
        self.btn_save_zip.clicked.connect(self.save_zip)
        self.btn_export_folder.clicked.connect(self.save_csvs_to_folder)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow { background: #f4f7fb; }
            QMenuBar {
                background: #ffffff;
                color: #14314d;
                border-bottom: 1px solid #dde6f0;
                padding: 4px 8px;
            }
            QMenuBar::item { background: transparent; color: #14314d; padding: 6px 10px; }
            QMenuBar::item:selected { background: #edf4fb; border-radius: 8px; }
            QMenu {
                background: #ffffff;
                color: #14314d;
                border: 1px solid #d9e4ef;
                padding: 6px;
            }
            QMenu::item { padding: 8px 12px; border-radius: 8px; }
            QMenu::item:selected { background: #edf4fb; }
            QGroupBox {
                background: #ffffff;
                border: 1px solid #dfe8f1;
                border-radius: 16px;
                margin-top: 10px;
                font-size: 14px;
                font-weight: 700;
                color: #16324f;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
            QLabel {
                color: #24415f;
                font-size: 13px;
                background: transparent;
            }
            QLabel#fieldLabel { color: #16324f; font-weight: 700; }
            QLineEdit, QComboBox, QSpinBox, QTextEdit, QTableWidget {
                background: #ffffff;
                color: #14314d;
                selection-background-color: #dbeeff;
                selection-color: #10283f;
                border: 1px solid #ced9e5;
                border-radius: 10px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus, QTableWidget:focus {
                border: 1px solid #0e5ea8;
            }
            QComboBox::drop-down {
                border: none;
                width: 26px;
            }
            QComboBox QAbstractItemView {
                background: #ffffff;
                color: #14314d;
                selection-background-color: #dbeeff;
                selection-color: #10283f;
                border: 1px solid #ced9e5;
                outline: 0;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: #f7fafc;
                border-left: 1px solid #d8e2ec;
                width: 18px;
            }
            QCheckBox {
                color: #16324f;
                spacing: 8px;
                font-weight: 600;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 5px;
                border: 1px solid #9eb6cb;
                background: #ffffff;
            }
            QCheckBox::indicator:checked {
                background: #0e5ea8;
                border: 1px solid #0e5ea8;
            }
            QHeaderView::section {
                background: #edf3f9;
                color: #16324f;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #dbe5ef;
                font-weight: 700;
            }
            QTableWidget {
                gridline-color: #ebf1f6;
                alternate-background-color: #f8fbfe;
            }
            QTableWidget::item {
                color: #16324f;
                padding: 6px;
            }
            QTableWidget::item:selected {
                background: #dbeeff;
                color: #10283f;
            }
            QPushButton {
                background: #ffffff;
                color: #16324f;
                border: 1px solid #c8d5e3;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: 700;
                min-height: 18px;
            }
            QPushButton:hover { background: #f0f6fc; }
            QPushButton:pressed { background: #e6f0fa; }
            QPushButton:disabled {
                background: #f2f5f8;
                color: #95a7ba;
                border: 1px solid #d9e1e9;
            }
            QPushButton#primaryButton {
                background: #0e5ea8;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover { background: #0b4f8f; }
            QPushButton#primaryButton:pressed { background: #083d6f; }
            QStatusBar {
                background: #ffffff;
                color: #49637f;
                border-top: 1px solid #dde6f0;
            }
            QFrame#headerCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d4b87, stop:1 #0d876b);
                border-radius: 22px;
            }
            QLabel#logoBadge {
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.14);
                border-radius: 18px;
                padding: 4px;
            }
            QLabel#heroIcon { font-size: 38px; color: white; }
            QLabel#heroTitle { color: white; font-size: 28px; font-weight: 800; }
            QLabel#heroSubtitle { color: rgba(255,255,255,0.92); font-size: 14px; font-weight: 600; }
            QLabel#heroHelper { color: rgba(255,255,255,0.78); font-size: 12px; }
            QLabel#badge {
                color: #0d4b87;
                background: rgba(255,255,255,0.94);
                border-radius: 17px;
                font-size: 12px;
                font-weight: 800;
                padding: 0 12px;
            }
            QLabel#statusPill {
                color: white;
                background: rgba(255,255,255,0.16);
                border: 1px solid rgba(255,255,255,0.20);
                border-radius: 15px;
                font-size: 11px;
                font-weight: 800;
                padding: 0 12px;
            }
            QFrame#metricCard {
                background: #f8fbfe;
                border: 1px solid #dbe7f3;
                border-radius: 14px;
            }
            QLabel#metricTitle { color: #5b7590; font-size: 12px; font-weight: 700; }
            QLabel#metricValue { color: #0f2743; font-size: 24px; font-weight: 800; }
            QLabel#mutedText { color: #647a92; }
            QTabWidget::pane {
                border: 1px solid #dfe8f1;
                border-radius: 12px;
                background: white;
                top: -1px;
            }
            QTabBar::tab {
                background: #edf3f9;
                border: 1px solid #dce6f1;
                padding: 9px 14px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #264462;
                font-weight: 700;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom-color: #ffffff;
            }
            QScrollBar:vertical {
                background: #f3f7fb;
                width: 12px;
                margin: 12px 0 12px 0;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c5d5e5;
                min-height: 24px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
                border: none;
            }
            """
        )

    def select_excel(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar planilha preenchida",
            str(Path.home()),
            "Excel (*.xlsx)",
        )
        if not file_path:
            return
        self.selected_file = Path(file_path)
        self.lbl_selected_file.setText(str(self.selected_file))
        self.statusBar().showMessage("Planilha selecionada.")
        self._log(f"Planilha selecionada: {self.selected_file.name}")
        self._update_generate_state()

    def save_template_copy(self) -> None:
        if not TEMPLATE_PATH.exists():
            self._show_error("Modelo não encontrado na pasta da aplicação.")
            return
        target, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar modelo Excel",
            str(Path.home() / "modelo_taxas_cartao_melhorado.xlsx"),
            "Excel (*.xlsx)",
        )
        if not target:
            return
        shutil.copyfile(TEMPLATE_PATH, target)
        self.statusBar().showMessage("Modelo salvo com sucesso.")
        self._log(f"Modelo salvo em: {target}")

    def open_app_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(BASE_DIR)))

    def _collect_params(self) -> AppParams:
        return AppParams(
            tipo_recebimento=self.cmb_tipo_recebimento.currentText(),
            liberada_cons_final_padrao=self.cmb_liberada.currentText(),
            credenciadora_id=int(self.spn_credenciadora_id.value()),
            utilizar_em_vendas_web=self.cmb_vendas_web.currentText(),
            forma_calc_dif_cartao_parc=self.cmb_forma_calc.currentText(),
            perm_vincular_crt_aut_caixa=self.cmb_perm_vincular.currentText(),
            tipo_vencimento_parcelas=self.cmb_tipo_venc_parcelas.currentText(),
            dia_inicio_periodo_vencimento=self.cmb_dia_inicio.currentText(),
            dias_para_venc_primeira_parc=self.cmb_dias_primeira.currentText(),
            tipo_parcelamento=self.cmb_tipo_parcelamento.currentText(),
            tipo_cobranca_retencao=self.cmb_tipo_cobranca.currentText(),
            vencimento_parc_prox_dia_util=self.cmb_venc_prox_util.currentText(),
            recebimento_unico_pag_seguro="S" if self.chk_receb_unico.isChecked() else "N",
            apenas_dias_uteis_calculo_prazo="S" if self.chk_apenas_uteis.isChecked() else "N",
            tipo_inicio_periodo_vencimento=self.cmb_tipo_inicio_periodo.currentText(),
            tipo_vencimento_primeira_parc=self.cmb_tipo_venc_primeira.currentText(),
        )

    def generate_outputs(self) -> None:
        if not self.selected_file:
            self._show_warning("Selecione uma planilha antes de gerar os arquivos.")
            return
        try:
            file_bytes = self.selected_file.read_bytes()
            params = self._collect_params()
            self.outputs = build_outputs(file_bytes, params)
            self.last_zip_bytes = build_zip(self.outputs)
            self._populate_tables(self.outputs)
            self._update_metrics(self.outputs)
            self._log("Arquivos gerados com sucesso.")
            self._log("Use 'Salvar ZIP' ou 'Salvar CSVs em pasta' para exportar o resultado.")
            self.statusBar().showMessage("Arquivos gerados com sucesso.")
        except ValidationError as exc:
            self._show_error(str(exc))
        except Exception as exc:
            self._show_error(f"Erro inesperado: {exc}")

    def _populate_tables(self, outputs: Dict[str, pd.DataFrame]) -> None:
        for filename, table in self.tables.items():
            df = outputs.get(filename, pd.DataFrame())
            table.clear()
            table.setColumnCount(len(df.columns))
            table.setRowCount(len(df.index))
            table.setHorizontalHeaderLabels([str(c) for c in df.columns])

            for row_idx in range(len(df.index)):
                for col_idx, column in enumerate(df.columns):
                    value = df.iloc[row_idx, col_idx]
                    item = QTableWidgetItem("" if pd.isna(value) else str(value))
                    table.setItem(row_idx, col_idx, item)

            table.resizeColumnsToContents()

    def _update_metrics(self, outputs: Dict[str, pd.DataFrame]) -> None:
        cards = {
            "portadores.csv": self.metric_portadores,
            "cartoes.csv": self.metric_cartoes,
            "prazos.csv": self.metric_prazos,
            "retencoes.csv": self.metric_retencoes,
        }
        for filename, widget in cards.items():
            value = str(len(outputs.get(filename, pd.DataFrame()).index))
            widget.metric_value.setText(value)  # type: ignore[attr-defined]

    def save_zip(self) -> None:
        if not self.last_zip_bytes:
            self._show_warning("Gere os arquivos antes de salvar o ZIP.")
            return
        target, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar ZIP gerado",
            str(Path.home() / "layout_importacartao_saida.zip"),
            "ZIP (*.zip)",
        )
        if not target:
            return
        Path(target).write_bytes(self.last_zip_bytes)
        self.statusBar().showMessage("ZIP salvo com sucesso.")
        self._log(f"ZIP salvo em: {target}")

    def save_csvs_to_folder(self) -> None:
        if not self.outputs:
            self._show_warning("Gere os arquivos antes de salvar os CSVs.")
            return
        target_dir = QFileDialog.getExistingDirectory(self, "Selecionar pasta para salvar os CSVs", str(Path.home()))
        if not target_dir:
            return
        out_dir = Path(target_dir)
        for filename, df in self.outputs.items():
            (out_dir / filename).write_text(df.to_csv(index=False, sep=";", encoding="utf-8-sig"), encoding="utf-8-sig")
        self.statusBar().showMessage("CSVs salvos com sucesso.")
        self._log(f"CSVs salvos em: {out_dir}")

    def _update_generate_state(self) -> None:
        self.btn_generate.setEnabled(self.selected_file is not None)

    def _log(self, message: str) -> None:
        self.txt_log.append(message)

    def _show_warning(self, message: str) -> None:
        QMessageBox.warning(self, APP_NAME, message)
        self._log(message)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, APP_NAME, message)
        self.statusBar().showMessage("Erro ao processar a operação.")
        self._log(message)


def configure_application(app: QApplication) -> None:
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("OpenAI")
    if LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(LOGO_PATH)))

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#f4f7fb"))
    palette.setColor(QPalette.WindowText, QColor("#14314d"))
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.AlternateBase, QColor("#f8fbfe"))
    palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
    palette.setColor(QPalette.ToolTipText, QColor("#14314d"))
    palette.setColor(QPalette.Text, QColor("#14314d"))
    palette.setColor(QPalette.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ButtonText, QColor("#14314d"))
    palette.setColor(QPalette.BrightText, QColor("#ffffff"))
    palette.setColor(QPalette.Highlight, QColor("#dbeeff"))
    palette.setColor(QPalette.HighlightedText, QColor("#10283f"))
    palette.setColor(QPalette.Link, QColor("#0e5ea8"))
    app.setPalette(palette)


def main() -> int:
    app = QApplication(sys.argv)
    configure_application(app)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
