from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QGroupBox, QVBoxLayout, QSizePolicy, QSpinBox
from app.utils.parsing import normalize_text

from app.domain.mappings import (
    FORMA_CALC_DIF_CARTAO_PARC_OPTIONS,
    TIPO_COBRANCA_RETENCAO_OPTIONS,
    TIPO_INICIO_PERIODO_VENCIMENTO_OPTIONS,
    TIPO_PARCELAMENTO_OPTIONS,
    TIPO_RECEBIMENTO_OPTIONS,
    TIPO_VENCIMENTO_PARCELAS_OPTIONS,
    TIPO_VENCIMENTO_PRIMEIRA_PARC_OPTIONS,
)
from app.domain.models import AppParams
from app.ui.widgets.form_fields import (
    add_labeled_widget,
    create_checkbox,
    create_combo_from_options,
    create_spinbox,
)
from app.ui.widgets.section_header import SectionHeader


class ParametersWidget(QGroupBox):
    """
    Painel com os parâmetros complementares da importação.

    A planilha traz os dados variáveis; este painel reúne as escolhas
    operacionais feitas pelo usuário antes da geração dos arquivos.
    """

    def __init__(self) -> None:
        super().__init__()

        self.root = QVBoxLayout(self)
        self.root.setSpacing(16)
        self.root.setContentsMargins(14, 18, 14, 14)
        self.root.addWidget(
            SectionHeader("Parâmetros da importação")
        )

        self.credenciadora_inputs: dict[str, QSpinBox] = {}

        self._build_general_section()
        self._build_credenciadoras_section()
        self._build_financial_rules_section()
        self._build_due_type_section()
        self._build_period_start_section()
        self._build_first_due_section()

        self._connect_signals()
        self._apply_initial_state()
        self._apply_control_sizes()

    # ========================================================
    # Seções principais
    # ========================================================
    def _build_general_section(self) -> None:
        self.box_geral = self._create_section_box("Geral")
        grid = self._create_grid()

        self.cmb_tipo_recebimento = create_combo_from_options(
            TIPO_RECEBIMENTO_OPTIONS, "POS"
        )

        self.chk_liberada = create_checkbox(
            "Venda liberada para consumidor final", True
        )
        self.chk_vendas_web = create_checkbox("Utilizar em vendas web", True)
        self.chk_perm_vincular = create_checkbox(
            "Permitir que este cartão seja vinculado automaticamente", True
        )
        self.chk_venc_prox_util = create_checkbox(
            "Vencimento da parcela sempre no próximo dia útil", True
        )
        self.chk_apenas_uteis = create_checkbox(
            "Considerar apenas dias uteis no calculo do prazo", False
        )
        self.chk_receb_unico = create_checkbox(
            "Recebimento unico (Pagseguro / Rede)", False
        )

        add_labeled_widget(grid, 0, 0, "Tipo de recebimento", self.cmb_tipo_recebimento)

        grid.addWidget(self.chk_liberada, 1, 0, 1, 4)
        grid.addWidget(self.chk_vendas_web, 2, 0, 1, 4)
        grid.addWidget(self.chk_perm_vincular, 3, 0, 1, 4)
        grid.addWidget(self.chk_venc_prox_util, 4, 0, 1, 4)
        grid.addWidget(self.chk_apenas_uteis, 5, 0, 1, 4)
        grid.addWidget(self.chk_receb_unico, 6, 0, 1, 4)

        self.box_geral.layout().addLayout(grid)
        self.root.addWidget(self.box_geral)

    def _build_financial_rules_section(self) -> None:
        self.box_regras = self._create_section_box("Parcelamento e retenção")
        grid = self._create_grid()

        self.cmb_forma_calc = create_combo_from_options(
            FORMA_CALC_DIF_CARTAO_PARC_OPTIONS, "A"
        )
        self.cmb_tipo_parcelamento = create_combo_from_options(
            TIPO_PARCELAMENTO_OPTIONS, "L"
        )
        self.cmb_tipo_cobranca = create_combo_from_options(
            TIPO_COBRANCA_RETENCAO_OPTIONS, "P"
        )

        add_labeled_widget(
            grid,
            0,
            0,
            "Forma de cálculo",
            self.cmb_forma_calc,
        )
        add_labeled_widget(
            grid,
            1,
            0,
            "Tipo do parcelamento",
            self.cmb_tipo_parcelamento,
        )
        add_labeled_widget(
            grid,
            2,
            0,
            "Tipo de cobrança da retenção",
            self.cmb_tipo_cobranca,
        )

        self.box_regras.layout().addLayout(grid)
        self.root.addWidget(self.box_regras)

    def _build_due_type_section(self) -> None:
        self.box_venc = self._create_section_box("Vencimento das parcelas")
        grid = self._create_grid()

        self.cmb_tipo_venc_parcelas = create_combo_from_options(
            TIPO_VENCIMENTO_PARCELAS_OPTIONS, "U"
        )

        add_labeled_widget(
            grid,
            0,
            0,
            "Tipo de vencimento das parcelas",
            self.cmb_tipo_venc_parcelas,
        )

        self.box_venc.layout().addLayout(grid)
        self.root.addWidget(self.box_venc)

    def _build_period_start_section(self) -> None:
        self.box_inicio = self._create_section_box("Data inicial do periodo de vencimento")
        grid = self._create_grid()

        self.cmb_tipo_inicio_periodo = create_combo_from_options(
            TIPO_INICIO_PERIODO_VENCIMENTO_OPTIONS, "V"
        )
        self.spn_dia_inicio_periodo = create_spinbox(0, 31, 0)

        add_labeled_widget(
            grid,
            0,
            0,
            "Tipo",
            self.cmb_tipo_inicio_periodo,
        )
        add_labeled_widget(
            grid,
            0,
            2,
            "Dia do mês",
            self.spn_dia_inicio_periodo,
        )

        self.box_inicio.layout().addLayout(grid)
        self.root.addWidget(self.box_inicio)

    def _build_first_due_section(self) -> None:
        self.box_primeira = self._create_section_box("Vencimento da primeira parcela")
        grid = self._create_grid()

        self.cmb_tipo_venc_primeira = create_combo_from_options(
            TIPO_VENCIMENTO_PRIMEIRA_PARC_OPTIONS, "M"
        )
        self.spn_dias_primeira = create_spinbox(0, 365, 0)

        add_labeled_widget(
            grid,
            0,
            0,
            "Tipo",
            self.cmb_tipo_venc_primeira,
        )
        add_labeled_widget(
            grid,
            0,
            2,
            "Qtd. de dias",
            self.spn_dias_primeira,
        )

        self.box_primeira.layout().addLayout(grid)
        self.root.addWidget(self.box_primeira)

    def _build_credenciadoras_section(self) -> None:
        self.box_credenciadoras = self._create_section_box("Credenciadoras")
        self.credenciadoras_grid = self._create_grid()

        self.box_credenciadoras.layout().addLayout(self.credenciadoras_grid)
        self.root.addWidget(self.box_credenciadoras)

        self.box_credenciadoras.setVisible(False)
    
    # ========================================================
    # Helpers visuais / construção
    # ========================================================
    def _create_section_box(self, title: str) -> QGroupBox:
        box = QGroupBox()
        layout = QVBoxLayout(box)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(SectionHeader(title))
        return box

    @staticmethod
    def _create_grid() -> QGridLayout:
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        grid.setColumnStretch(3, 1)

        return grid

    def _apply_control_sizes(self) -> None:
        for combo in [
            self.cmb_tipo_recebimento,
            self.cmb_forma_calc,
            self.cmb_tipo_parcelamento,
            self.cmb_tipo_cobranca,
            self.cmb_tipo_venc_parcelas,
            self.cmb_tipo_inicio_periodo,
            self.cmb_tipo_venc_primeira,
        ]:
            combo.setMinimumHeight(36)
            combo.setMinimumWidth(0)
            combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        for spin in [
            self.spn_dia_inicio_periodo,
            self.spn_dias_primeira,
        ]:
            spin.setMinimumHeight(36)
            spin.setMinimumWidth(0)
            spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    # ========================================================
    # Helpers de leitura dos valores
    # ========================================================
    @staticmethod
    def _checkbox_value(checkbox) -> str:
        return "S" if checkbox.isChecked() else "N"

    @staticmethod
    def _combo_value(combo) -> str:
        return str(combo.currentData())

    def _set_combo_by_value(self, combo, value: str) -> None:
        index = combo.findData(value)
        if index >= 0:
            combo.setCurrentIndex(index)

    def set_credenciadoras(self, credenciadoras: list[str]) -> None:
        self.credenciadora_inputs.clear()

        while self.credenciadoras_grid.count():
            item = self.credenciadoras_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        credenciadoras_normalizadas = sorted({
            normalize_text(cred)
            for cred in credenciadoras
            if normalize_text(cred)
        })

        if not credenciadoras_normalizadas:
            self.box_credenciadoras.setVisible(False)
            return

        for row, credenciadora in enumerate(credenciadoras_normalizadas):
            spin = create_spinbox(1, 999999, 1)
            spin.setMinimumHeight(36)
            spin.setMinimumWidth(0)
            spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            self.credenciadora_inputs[credenciadora] = spin
            add_labeled_widget(
                self.credenciadoras_grid,
                row,
                0,
                f"{credenciadora} ID",
                spin,
            )

        self.box_credenciadoras.setVisible(True)

    # ========================================================
    # Regras de comportamento entre campos
    # ========================================================
    def _connect_signals(self) -> None:
        self.cmb_tipo_venc_parcelas.currentIndexChanged.connect(
            self._on_tipo_vencimento_parcelas_changed
        )
        self.cmb_tipo_inicio_periodo.currentIndexChanged.connect(
            self._on_tipo_inicio_changed
        )
        self.cmb_tipo_venc_primeira.currentIndexChanged.connect(
            self._on_tipo_primeira_changed
        )

    def _apply_initial_state(self) -> None:
        self._on_tipo_vencimento_parcelas_changed()
        self._on_tipo_inicio_changed()
        self._on_tipo_primeira_changed()

    def _on_tipo_vencimento_parcelas_changed(self) -> None:
        codigo = self._combo_value(self.cmb_tipo_venc_parcelas)
        ocultar_blocos = codigo == "U"

        if ocultar_blocos:
            self._set_combo_by_value(self.cmb_tipo_inicio_periodo, "V")
            self.spn_dia_inicio_periodo.setValue(0)
            self._set_combo_by_value(self.cmb_tipo_venc_primeira, "M")
            self.spn_dias_primeira.setValue(0)

        self.box_inicio.setVisible(not ocultar_blocos)
        self.box_primeira.setVisible(not ocultar_blocos)

        self.cmb_tipo_inicio_periodo.setEnabled(not ocultar_blocos)
        self.spn_dia_inicio_periodo.setEnabled(not ocultar_blocos)
        self.cmb_tipo_venc_primeira.setEnabled(not ocultar_blocos)
        self.spn_dias_primeira.setEnabled(not ocultar_blocos)

    def _on_tipo_inicio_changed(self) -> None:
        if not self.cmb_tipo_inicio_periodo.isEnabled():
            return

        codigo = self._combo_value(self.cmb_tipo_inicio_periodo)
        if codigo == "V":
            self.spn_dia_inicio_periodo.setValue(0)
            self.spn_dia_inicio_periodo.setEnabled(False)
            self.spn_dia_inicio_periodo.setValue(0)
            self.spn_dia_inicio_periodo.setEnabled(False)
        else:
            self.spn_dia_inicio_periodo.setEnabled(True)

    def _on_tipo_primeira_changed(self) -> None:
        if not self.cmb_tipo_venc_primeira.isEnabled():
            return

        codigo = self._combo_value(self.cmb_tipo_venc_primeira)
        if codigo == "M":
            self.spn_dias_primeira.setValue(0)
            self.spn_dias_primeira.setEnabled(False)
        else:
            self.spn_dias_primeira.setEnabled(True)

    def get_credenciadora_ids(self) -> dict[str, int]:
        return {
            credenciadora: spin.value()
            for credenciadora, spin in self.credenciadora_inputs.items()
        }
    
    # ========================================================
    # Saída estruturada dos parâmetros
    # ========================================================
    def get_params(self) -> AppParams:
        return AppParams(
            tipo_recebimento=self._combo_value(self.cmb_tipo_recebimento),
            liberada_cons_final_padrao=self._checkbox_value(self.chk_liberada),
            credenciadora_ids=self.get_credenciadora_ids(),
            utilizar_em_vendas_web=self._checkbox_value(self.chk_vendas_web),
            forma_calc_dif_cartao_parc=self._combo_value(self.cmb_forma_calc),
            perm_vincular_crt_aut_caixa=self._checkbox_value(self.chk_perm_vincular),
            tipo_vencimento_parcelas=self._combo_value(self.cmb_tipo_venc_parcelas),
            dia_inicio_periodo_vencimento=self.spn_dia_inicio_periodo.value(),
            dias_para_venc_primeira_parc=self.spn_dias_primeira.value(),
            tipo_parcelamento=self._combo_value(self.cmb_tipo_parcelamento),
            tipo_cobranca_retencao=self._combo_value(self.cmb_tipo_cobranca),
            vencimento_parc_prox_dia_util=self._checkbox_value(self.chk_venc_prox_util),
            recebimento_unico_pag_seguro=self._checkbox_value(self.chk_receb_unico),
            apenas_dias_uteis_calculo_prazo=self._checkbox_value(self.chk_apenas_uteis),
            tipo_inicio_periodo_vencimento=self._combo_value(self.cmb_tipo_inicio_periodo),
            tipo_vencimento_primeira_parc=self._combo_value(self.cmb_tipo_venc_primeira),
        )