from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, 
    QComboBox, 
    QGridLayout, 
    QGroupBox, 
    QHBoxLayout,
    QLabel, 
    QSpinBox,
    QVBoxLayout,
    QWidget,)

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


class ParametersWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("3. Parâmetros da importação")

        root = QVBoxLayout(self)
        root.setSpacing(14)

        # ===== Seção geral =====
        box_geral = QGroupBox("Geral")
        grid_geral = QGridLayout(box_geral)
        grid_geral.setHorizontalSpacing(14)
        grid_geral.setVerticalSpacing(10)

        self.cmb_tipo_recebimento = self._combo_from_options(TIPO_RECEBIMENTO_OPTIONS, "POS")
        self.spn_credenciadora_id = QSpinBox()
        self.spn_credenciadora_id.setRange(1, 999999)
        self.spn_credenciadora_id.setValue(42)

        self.chk_liberada = QCheckBox("Venda liberada para consumidor final")
        self.chk_liberada.setChecked(True)

        self.chk_vendas_web = QCheckBox("Utilizar em vendas web")
        self.chk_vendas_web.setChecked(True)

        self.chk_perm_vincular = QCheckBox("Permitir que este cartão seja vinculado automaticamente")
        self.chk_perm_vincular.setChecked(True)

        self.chk_venc_prox_util = QCheckBox("Vencimento da parcela sempre no próximo dia útil")
        self.chk_venc_prox_util.setChecked(True)

        self.chk_apenas_uteis = QCheckBox("Considerar apenas dias uteis no calculo do prazo")
        self.chk_apenas_uteis.setChecked(False)

        self.chk_receb_unico = QCheckBox("Recebimento unico (Pagseguro / Rede)")
        self.chk_receb_unico.setChecked(False)

        grid_geral.addWidget(QLabel("Tipo de recebimento"), 0, 0)
        grid_geral.addWidget(self.cmb_tipo_recebimento, 0, 1)
        grid_geral.addWidget(QLabel("Credenciadora ID"), 0, 2)
        grid_geral.addWidget(self.spn_credenciadora_id, 0, 3)

        grid_geral.addWidget(self.chk_liberada, 1, 0, 1, 2)
        grid_geral.addWidget(self.chk_vendas_web, 1, 2, 1, 2)

        grid_geral.addWidget(self.chk_perm_vincular, 2, 0, 1, 2)
        grid_geral.addWidget(self.chk_venc_prox_util, 2, 2, 1, 2)

        grid_geral.addWidget(self.chk_apenas_uteis, 3, 0, 1, 2)
        grid_geral.addWidget(self.chk_receb_unico, 3, 2, 1, 2)

        root.addWidget(box_geral)

        # ===== Seção parcelamento e retenção =====
        box_parc = QGroupBox("Parcelamento e retenção")
        grid_parc = QGridLayout(box_parc)
        grid_parc.setHorizontalSpacing(14)
        grid_parc.setVerticalSpacing(10)

        self.cmb_forma_calc = self._combo_from_options(FORMA_CALC_DIF_CARTAO_PARC_OPTIONS, "A")
        self.cmb_tipo_parcelamento = self._combo_from_options(TIPO_PARCELAMENTO_OPTIONS, "L")
        self.cmb_tipo_cobranca = self._combo_from_options(TIPO_COBRANCA_RETENCAO_OPTIONS, "P")

        grid_parc.addWidget(QLabel("Forma de cálculo (cartão parcelado)"), 0, 0)
        grid_parc.addWidget(self.cmb_forma_calc, 0, 1)

        grid_parc.addWidget(QLabel("Tipo do parcelamento"), 0, 2)
        grid_parc.addWidget(self.cmb_tipo_parcelamento, 0, 3)

        grid_parc.addWidget(QLabel("Tipo de cobrança da retenção"), 1, 0)
        grid_parc.addWidget(self.cmb_tipo_cobranca, 1, 1)

        root.addWidget(box_parc)

        # ===== Seção vencimento =====
        box_venc = QGroupBox("Vencimento das parcelas")
        grid_venc = QGridLayout(box_venc)
        grid_venc.setHorizontalSpacing(14)
        grid_venc.setVerticalSpacing(10)

        self.cmb_tipo_venc_parcelas = self._combo_from_options(TIPO_VENCIMENTO_PARCELAS_OPTIONS, "U")

        grid_venc.addWidget(QLabel("Tipo de vencimento das parcelas"), 0, 0)
        grid_venc.addWidget(self.cmb_tipo_venc_parcelas, 0, 1)

        root.addWidget(box_venc)

        # ===== Seção data inicial =====
        box_inicio = QGroupBox("Data inicial do periodo de vencimento")
        grid_inicio = QGridLayout(box_inicio)
        grid_inicio.setHorizontalSpacing(14)
        grid_inicio.setVerticalSpacing(10)

        self.cmb_tipo_inicio_periodo = self._combo_from_options(TIPO_INICIO_PERIODO_VENCIMENTO_OPTIONS, "V")

        self.spn_dia_inicio_periodo = QSpinBox()
        self.spn_dia_inicio_periodo.setRange(0, 31)
        self.spn_dia_inicio_periodo.setValue(0)

        grid_inicio.addWidget(QLabel("Tipo Data inicial do periodo de vencimento"), 0, 0)
        grid_inicio.addWidget(self.cmb_tipo_inicio_periodo, 0, 1)
        grid_inicio.addWidget(QLabel("Data inicial do periodo de vencimento"), 0, 2)
        grid_inicio.addWidget(self.spn_dia_inicio_periodo, 0, 3)

        root.addWidget(box_inicio)

        # ===== Seção primeira parcela =====
        box_primeira = QGroupBox("Vencimento da primeira parcela")
        grid_primeira = QGridLayout(box_primeira)
        grid_primeira.setHorizontalSpacing(14)
        grid_primeira.setVerticalSpacing(10)

        self.cmb_tipo_venc_primeira = self._combo_from_options(TIPO_VENCIMENTO_PRIMEIRA_PARC_OPTIONS, "M")

        self.spn_dias_primeira = QSpinBox()
        self.spn_dias_primeira.setRange(0, 365)
        self.spn_dias_primeira.setValue(0)

        grid_primeira.addWidget(QLabel("Tipo vencimento primeira parcela"), 0, 0)
        grid_primeira.addWidget(self.cmb_tipo_venc_primeira, 0, 1)
        grid_primeira.addWidget(QLabel("Dia p/ venc. primeira parcela"), 0, 2)
        grid_primeira.addWidget(self.spn_dias_primeira, 0, 3)

        root.addWidget(box_primeira)

        # sinais
        self.cmb_tipo_venc_parcelas.currentIndexChanged.connect(self._on_tipo_vencimento_parcelas_changed)
        self.cmb_tipo_inicio_periodo.currentIndexChanged.connect(self._on_tipo_inicio_changed)
        self.cmb_tipo_venc_primeira.currentIndexChanged.connect(self._on_tipo_primeira_changed)

        # aplica estado inicial
        self._on_tipo_vencimento_parcelas_changed()
        self._on_tipo_inicio_changed()
        self._on_tipo_primeira_changed()

    @staticmethod
    def _combo_from_options(options: list[tuple[str, str]], current_value: str) -> QComboBox:
        combo = QComboBox()
        for label, value in options:
            combo.addItem(label, value)

        index = combo.findData(current_value)
        if index >= 0:
            combo.setCurrentIndex(index)
        return combo

    @staticmethod
    def _checkbox_value(checkbox: QCheckBox) -> str:
        return "S" if checkbox.isChecked() else "N"

    @staticmethod
    def _combo_value(combo: QComboBox) -> str:
        return str(combo.currentData())

    def _set_combo_by_value(self, combo: QComboBox, value: str) -> None:
        index = combo.findData(value)
        if index >= 0:
            combo.setCurrentIndex(index)

    def _on_tipo_vencimento_parcelas_changed(self) -> None:
        codigo = self._combo_value(self.cmb_tipo_venc_parcelas)
        bloquear = codigo == "U"

        if bloquear:
            self._set_combo_by_value(self.cmb_tipo_inicio_periodo, "V")
            self.spn_dia_inicio_periodo.setValue(0)

            self._set_combo_by_value(self.cmb_tipo_venc_primeira, "M")
            self.spn_dias_primeira.setValue(0)

        self.cmb_tipo_inicio_periodo.setEnabled(not bloquear)
        self.spn_dia_inicio_periodo.setEnabled(not bloquear)
        self.cmb_tipo_venc_primeira.setEnabled(not bloquear)
        self.spn_dias_primeira.setEnabled(not bloquear)

    def _on_tipo_inicio_changed(self) -> None:
        if not self.cmb_tipo_inicio_periodo.isEnabled():
            return

        codigo = self._combo_value(self.cmb_tipo_inicio_periodo)
        if codigo == "V":
            self.spn_dia_inicio_periodo.setValue(0)
            self.spn_dia_inicio_periodo.setEnabled(False)
        else:
            self.spn_dia_inicio_periodo.setEnabled(True)
            if self.spn_dia_inicio_periodo.value() == 0:
                self.spn_dia_inicio_periodo.setValue(1)

    def _on_tipo_primeira_changed(self) -> None:
        if not self.cmb_tipo_venc_primeira.isEnabled():
            return

        codigo = self._combo_value(self.cmb_tipo_venc_primeira)
        if codigo == "M":
            self.spn_dias_primeira.setValue(0)
            self.spn_dias_primeira.setEnabled(False)
        else:
            self.spn_dias_primeira.setEnabled(True)
            if self.spn_dias_primeira.value() == 0:
                self.spn_dias_primeira.setValue(1)

    def get_params(self) -> AppParams:
        return AppParams(
            tipo_recebimento=self._combo_value(self.cmb_tipo_recebimento),
            liberada_cons_final_padrao=self._checkbox_value(self.chk_liberada),
            credenciadora_id=self.spn_credenciadora_id.value(),
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