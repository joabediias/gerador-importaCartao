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
    "AGIPLAN": "AGIPLAN",
    "BANESCARD": "BANESCARD",
    "CREDSYSTEM": "CREDSYSTEM",
    "ESPLANADA": "ESPLANADA",
    "CREDZ": "CREDZ",
    "JCB": "JCB",
    "SICREDI": "SICREDI",
    "AVISTA": "AVISTA",
    "DISCOVER": "DISCOVER",
    "OUROCARD": "OUROCARD",
    "BANRICOMPRAS": "BANRICOMPRAS",
    "UNIONPAY": "UNIONPAY",
    "MAIS": "MAIS",
    "BNDS": "BNDS",
    "CUP": "CUP",
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
    "UNIONPAY": "UNI",
    "MAIS": "MAI",
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
    ("POS", "POS"),
    ("TEF", "TEF"),
    ("AMBOS", "AMBOS"),
]

FORMA_CALC_DIF_CARTAO_PARC_OPTIONS = [
    ("Arredondar", "A"),
    ("Truncar", "T"),
]

TIPO_VENCIMENTO_PARCELAS_OPTIONS = [
    ("Utiliza dias informados pelo usuário", "U"),
    ("Utiliza dia fixo", "F"),
]

TIPO_COBRANCA_RETENCAO_OPTIONS = [
    ("Parcela a parcela", "P"),
    ("Apenas na primeira parcela", "A"),
]

TIPO_PARCELAMENTO_OPTIONS = [
    ("Pelo lojista", "L"),
    ("Pela operadora", "O"),
]

TIPO_INICIO_PERIODO_VENCIMENTO_OPTIONS = [
    ("Data da venda", "V"),
    ("Dia do mes", "D"),
]

TIPO_VENCIMENTO_PRIMEIRA_PARC_OPTIONS = [
    ("Proximo mes", "M"),
    ("Qtd. de dias", "D"),
]

TIPO_RETENCAO_CARTAO_OPTIONS = [
    ("Getnet", "G"),
    ("Cielo", "C"),
    ("PagSeguro", "P"),
]

CREDENCIADORA_CNPJ_MAP = {
    "CIELO": "01027058000191",
    "REDE": "01425787000104",
    "REDECARD": "01425787000104",
    "GETNET": "10440482000154",
    "PAGSEGURO": "08561701000101",
    "PAG SEGURO": "08561701000101",
    "STONE": "16501555000157",
    "BIN": "04962772000165",
    "SAFRA PAY": "58160789000128",
    "SAFRAPAY": "58160789000128",
    "MERCADO PAGO": "10573521000191",
}