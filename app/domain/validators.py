from __future__ import annotations

from typing import Iterable

import pandas as pd

from .mappings import REQUIRED_COLUMNS


class ValidationError(Exception):
    pass


def ensure_columns(df: pd.DataFrame, required: Iterable[str] = REQUIRED_COLUMNS) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValidationError(f"Colunas obrigatórias ausentes na aba TAXAS: {', '.join(missing)}")


def ensure_not_empty(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValidationError("A aba TAXAS não possui linhas preenchidas.")


def validate_app_params(params) -> None:
    if params.tipo_vencimento_parcelas == "U":
        if params.tipo_inicio_periodo_vencimento != "V":
            raise ValidationError(
                "Quando o tipo de vencimento das parcelas for 'Utiliza dias informados pelo usuário', "
                "o tipo da data inicial do período de vencimento deve ser 'Data da venda'."
            )

        if params.dia_inicio_periodo_vencimento != 0:
            raise ValidationError(
                "Quando o tipo de vencimento das parcelas for 'Utiliza dias informados pelo usuário', "
                "a data inicial do período de vencimento deve ser 0."
            )

        if params.tipo_vencimento_primeira_parc != "M":
            raise ValidationError(
                "Quando o tipo de vencimento das parcelas for 'Utiliza dias informados pelo usuário', "
                "o tipo de vencimento da primeira parcela deve ser 'Proximo mes'."
            )

        if params.dias_para_venc_primeira_parc != 0:
            raise ValidationError(
                "Quando o tipo de vencimento das parcelas for 'Utiliza dias informados pelo usuário', "
                "o dia para vencimento da primeira parcela deve ser 0."
            )

    if params.tipo_inicio_periodo_vencimento == "V" and params.dia_inicio_periodo_vencimento != 0:
        raise ValidationError(
            "Se o tipo da data inicial do período de vencimento for 'Data da venda', o dia deve ser 0."
        )

    if params.tipo_inicio_periodo_vencimento == "D" and params.dia_inicio_periodo_vencimento <= 0:
        raise ValidationError(
            "Data inicial do período de vencimento: quando o tipo for 'Dia do mês', "
            "informe um valor maior que 0."
        )

    if params.tipo_vencimento_primeira_parc == "M" and params.dias_para_venc_primeira_parc != 0:
        raise ValidationError(
            "Se o tipo de vencimento da primeira parcela for 'Proximo mes', o dia deve ser 0."
        )

    if params.tipo_vencimento_primeira_parc == "D" and params.dias_para_venc_primeira_parc <= 0:
        raise ValidationError(
            "Vencimento da primeira parcela: quando o tipo for 'Qtd. de dias', "
            "informe um valor maior que 0."
        )
    
    if not params.credenciadora_cnpjs:
        raise ValidationError(
            "Informe o código das credenciadoras encontradas na planilha."
        )
    
    for credenciadora, cnpj in params.credenciadora_cnpjs.items():
        cnpj_limpo = str(cnpj).strip()
        
        if not cnpj_limpo:
            raise ValidationError(
                f"Informe o CNPJ da credenciadora '{credenciadora}'."
            )

        if len(cnpj_limpo) != 14:
            raise ValidationError(
                f"O CNPJ da credenciadora '{credenciadora}' deve ter 14 dígitos."
            )

        if not cnpj_limpo.isdigit():
            raise ValidationError(
                f"O CNPJ da credenciadora '{credenciadora}' deve conter apenas números."
            )