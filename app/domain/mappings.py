REQUIRED_COLUMNS = [
    "EMPRESAS",
    "CREDENCIADORA",
    "BANDEIRA",
    "DIAS_DEBITO",
    "DIAS_CREDITO",
    "DIAS_PARCELADO",
    "DEBITO",
    "1X",
]

BANDEIRA_TEF_MAP = {
    "MASTERCARD": "MASTERCARD",
    "AMEX": "AMEX",
    "AMERICAN EXPRESS": "AMEX",
    "HIPERCARD": "HIPERCARD",
    "HIPER": "HIPERCARD",
    "ELO": "ELO",
    "VISA": "VISA",
    "DINERS": "DINERS",
    "CABAL": "CABAL",
    "SOROCRED": "SOROCRED",
}

BANDEIRA_COD_MAP = {
    "VISA": "VIS",
    "MASTERCARD": "MAS",
    "SOROCRED": "SOR",
    "ELO": "ELO",
    "DINERS": "DIN",
    "AGIPLAN": "AGI",
    "BANESCARD": "BAN",
    "CABAL": "CAB",
    "CREDSYSTEM": "CRE",
    "ESPLANADA": "ESP",
    "CREDZ": "CRZ",
    "HIPERCARD": "HIP",
    "HIPER": "HPR",
    "CUP": "CUP",
    "SICREDI": "SIC",
    "AVISTA": "AVI",
    "AMEX": "AME",
    "AMERICAN EXPRESS": "AME",
    "DISCOVER": "DIS",
    "JCB": "JCB",
    "OUROCARD": "OUR",
    "BANRICOMPRAS": "BAR",
}

REDE_CREDITO_MAP = {
    "AMEX": "A",
    "AMERICAN EXPRESS": "A",
    "VISANET": "V",
    "REDE": "R",
    "REDECARD": "R",
    "HIPERCARD": "H",
    "HIPER": "H",
    "TECBAN": "T",
    "ELO": "E",
    "DINERS": "D",
    "AUTTAR": "U",
    "ENTREPLAY": "B",
    "CIELO": "C",
    "GETNET": "G",
    "PAGUE VELOZ": "P",
}

TIPO_RETENCAO_MAP = {
    "GETNET": "G",
    "CIELO": "C",
    "PAGSEGURO": "P",
    "PAG SEGURO": "P",
    "PAGSEGURO UOL": "P",
}

TIPO_RECEBIMENTO_OPTIONS = [
    "POS", "POS",
    "TEF", "TEF",
    "AMBOS", "AMBOS",
]

FORMA_CALC_DIF_CARTAO_PARC = {
    "Arredondar": "A",
    "Truncar": "T",
}

TIPO_VENCIMENTO_PARCELAS = {
    "Utiliza dias informados pelo usuário": "U",
    "Utiliza dia fixo": "F",
}

TIPO_COBRANCA_RETENCAO = {
    "Parcela a parcela": "P",
    "Apenas na primeira parcela": "A",
}

TIPO_PARCELAMENTO = {
    "Pelo lojista": "L",
    "Pela operadora": "O",
}

TIPO_INICIO_PERIODO_VENCIMENTO = {
    "Data da venda": "V",
    "Dia do mes": "D",
}

TIPO_VENCIMENTO_PRIMEIRA_PARC = {
    "Proximo mes": "M",
    "Qtd. de dias": "D",
}