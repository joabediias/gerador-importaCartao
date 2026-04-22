from app.domain.models import AppParams


def test_params_dataclass_smoke() -> None:
    params = AppParams(
        tipo_recebimento="POS",
        liberada_cons_final_padrao="S",
        credenciadora_id=42,
        utilizar_em_vendas_web="S",
        forma_calc_dif_cartao_parc="A",
        perm_vincular_crt_aut_caixa="S",
        tipo_vencimento_parcelas="U",
        dia_inicio_periodo_vencimento="V",
        dias_para_venc_primeira_parc="M",
        tipo_parcelamento="L",
        tipo_cobranca_retencao="P",
        vencimento_parc_prox_dia_util="S",
        recebimento_unico_pag_seguro="N",
        apenas_dias_uteis_calculo_prazo="N",
        tipo_inicio_periodo_vencimento="V",
        tipo_vencimento_primeira_parc="M",
    )
    assert params.credenciadora_id == 42