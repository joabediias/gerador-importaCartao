from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QGridLayout, QGroupBox, QLabel, QSpinBox

from app.domain.models import AppParams


class ParametersWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("3. Parâmetros da importação")
        grid = QGridLayout(self)
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
            row = idx // 2
            col = (idx % 2) * 2
            grid.addWidget(QLabel(label), row, col)
            grid.addWidget(widget, row, col + 1)

        base_row = (len(fields) + 1) // 2 + 1
        grid.addWidget(self.chk_receb_unico, base_row, 0, 1, 2)
        grid.addWidget(self.chk_apenas_uteis, base_row, 2, 1, 2)

    @staticmethod
    def _combo(items: list[str], current: str) -> QComboBox:
        combo = QComboBox()
        combo.addItems(items)
        combo.setCurrentText(current)
        return combo

    def get_params(self) -> AppParams:
        return AppParams(
            tipo_recebimento=self.cmb_tipo_recebimento.currentText(),
            liberada_cons_final_padrao=self.cmb_liberada.currentText(),
            credenciadora_id=self.spn_credenciadora_id.value(),
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
