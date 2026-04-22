from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Dict, List, Tuple
import re
import zipfile

import pandas as pd


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


@dataclass
class AppParams:
    tipo_recebimento: str
    liberada_cons_final_padrao: str
    credenciadora_id: int
    utilizar_em_vendas_web: str
    forma_calc_dif_cartao_parc: str
    perm_vincular_crt_aut_caixa: str
    tipo_vencimento_parcelas: str
    dia_inicio_periodo_vencimento: str
    dias_para_venc_primeira_parc: str
    tipo_parcelamento: str
    tipo_cobranca_retencao: str
    vencimento_parc_prox_dia_util: str
    recebimento_unico_pag_seguro: str
    apenas_dias_uteis_calculo_prazo: str
    tipo_inicio_periodo_vencimento: str
    tipo_vencimento_primeira_parc: str


class ValidationError(Exception):
    pass


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return re.sub(r"\s+", " ", text).upper()


def parse_numeric(value: object) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    text = str(value).strip()
    if not text or text == "-":
        return None
    text = text.replace("%", "").replace(" ", "")
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def parse_empresas(value: object) -> List[str]:
    text = str(value or "").strip()
    if not text:
        raise ValidationError("Campo EMPRESAS vazio em uma das linhas da aba TAXAS.")
    parts = [p.strip() for p in text.split(";") if p.strip()]
    if not parts:
        raise ValidationError(f"Não foi possível interpretar EMPRESAS: {text}")
    for part in parts:
        if not re.fullmatch(r"\d+", part):
            raise ValidationError(f"Empresa inválida em EMPRESAS: {text}. Use formato como 1;2;3")
    return parts


def rede_cartao_tef(credenciadora: str) -> str:
    if credenciadora == "CIELO":
        return "CIELO"
    if credenciadora in {"REDE", "REDECARD"}:
        return "REDECARD"
    return "GETNET"


def rede_cartao_credito(credenciadora: str) -> str:
    return REDE_CREDITO_MAP.get(credenciadora, "G")


def tipo_retencao_cartao(credenciadora: str) -> str:
    return TIPO_RETENCAO_MAP.get(credenciadora, "G")


def tipo_cartao(tipo: str) -> str:
    return "D" if tipo == "DEBITO" else "C"


def bandeira_tef(bandeira: str) -> str:
    return BANDEIRA_TEF_MAP.get(bandeira, bandeira)


def bandeira_cod(bandeira: str) -> str:
    return BANDEIRA_COD_MAP.get(bandeira, bandeira[:3])


def read_taxas_excel(file_bytes: bytes) -> pd.DataFrame:
    try:
        df = pd.read_excel(BytesIO(file_bytes), sheet_name="TAXAS", header=3)
    except Exception as exc:
        raise ValidationError(f"Não foi possível ler a aba TAXAS: {exc}") from exc

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValidationError(f"Colunas obrigatórias ausentes na aba TAXAS: {', '.join(missing)}")

    df = df.fillna("")
    df = df[df["EMPRESAS"].astype(str).str.strip() != ""].copy()
    if df.empty:
        raise ValidationError("A aba TAXAS não possui linhas preenchidas.")

    return df


def extract_rate_entries(df: pd.DataFrame) -> List[Dict[str, object]]:
    entries: List[Dict[str, object]] = []
    for idx, row in df.iterrows():
        excel_row = idx + 5
        cred = normalize_text(row.get("CREDENCIADORA"))
        bandeira = normalize_text(row.get("BANDEIRA"))
        empresas = parse_empresas(row.get("EMPRESAS"))

        if not cred:
            raise ValidationError(f"Linha {excel_row}: CREDENCIADORA não informada.")
        if not bandeira:
            raise ValidationError(f"Linha {excel_row}: BANDEIRA não informada.")

        dias_debito = row.get("DIAS_DEBITO")
        dias_credito = row.get("DIAS_CREDITO")
        dias_parcelado = row.get("DIAS_PARCELADO")

        deb = parse_numeric(row.get("DEBITO"))
        if deb is not None:
            entries.append(
                {
                    "credenciadora": cred,
                    "bandeira": bandeira,
                    "tipo": "DEBITO",
                    "parcelas": 1,
                    "taxa": deb,
                    "dias": int(dias_debito) if str(dias_debito).strip() else 0,
                    "empresas": empresas,
                    "source_row": excel_row,
                }
            )

        credit = parse_numeric(row.get("1X"))
        if credit is not None:
            entries.append(
                {
                    "credenciadora": cred,
                    "bandeira": bandeira,
                    "tipo": "CREDITO",
                    "parcelas": 1,
                    "taxa": credit,
                    "dias": int(dias_credito) if str(dias_credito).strip() else 0,
                    "empresas": empresas,
                    "source_row": excel_row,
                }
            )

        for parcela in range(2, 25):
            rate = parse_numeric(row.get(f"{parcela}X"))
            if rate is None:
                continue
            entries.append(
                {
                    "credenciadora": cred,
                    "bandeira": bandeira,
                    "tipo": "PARCELADO",
                    "parcelas": parcela,
                    "taxa": rate,
                    "dias": int(dias_parcelado) if str(dias_parcelado).strip() else 0,
                    "empresas": empresas,
                    "source_row": excel_row,
                }
            )

    if not entries:
        raise ValidationError("Nenhuma taxa válida foi encontrada na aba TAXAS.")
    return entries


def build_portadores(entries: List[Dict[str, object]]) -> Tuple[pd.DataFrame, Dict[Tuple[str, str, str], int]]:
    seen: Dict[Tuple[str, str, str], int] = {}
    rows = []
    next_id = 8000
    for entry in entries:
        key = (entry["credenciadora"], entry["bandeira"], entry["tipo"])
        if key in seen:
            continue
        seen[key] = next_id
        rows.append(
            {
                "PORTADOR_ID": next_id,
                "NOME": f"{entry['bandeira']} {entry['tipo']} - {entry['credenciadora']}",
            }
        )
        next_id += 1
    return pd.DataFrame(rows), seen


def build_nome_cartao(cred: str, bandeira: str, tipo: str, parcelas: int) -> str:
    suffix = f" {parcelas:02d}X" if tipo == "PARCELADO" else ""
    return f"{cred} - {bandeira} {tipo}{suffix}"


def recebimento_variants(tipo_recebimento: str) -> List[str]:
    if tipo_recebimento == "AMBOS":
        return ["POS", "TEF"]
    return [tipo_recebimento]


def build_outputs(file_bytes: bytes, params: AppParams) -> Dict[str, pd.DataFrame]:
    taxas_df = read_taxas_excel(file_bytes)
    entries = extract_rate_entries(taxas_df)
    portadores_df, portador_map = build_portadores(entries)

    cartoes_rows = []
    prazos_rows = []
    retencoes_rows = []
    sequence = 1

    for entry in entries:
        for recebimento in recebimento_variants(params.tipo_recebimento):
            chave = f"{entry['credenciadora']}{sequence}"
            sequence += 1
            portador_id = portador_map[(entry["credenciadora"], entry["bandeira"], entry["tipo"])]
            cartoes_rows.append(
                {
                    "CHAVE_IMPORTACAO": chave,
                    "NOME": build_nome_cartao(entry["credenciadora"], entry["bandeira"], entry["tipo"], int(entry["parcelas"])),
                    "NUMERO_CONTRATO": "X",
                    "REDE_CARTAO_TEF": rede_cartao_tef(str(entry["credenciadora"])),
                    "BANDEIRA_CARTAO_TEF": bandeira_tef(str(entry["bandeira"])),
                    "PORTADOR_ID": portador_id,
                    "TIPO_CARTAO": tipo_cartao(str(entry["tipo"])),
                    "TIPO_RECEBIMENTO": recebimento,
                    "ATIVO": "S",
                    "PARCELAS": int(entry["parcelas"]),
                    "AJUSTAR_PARC_CART_IMP_FISCAL": "S",
                    "LIBERADA_CONS_FINAL_PADRAO": params.liberada_cons_final_padrao,
                    "REDE_CARTAO_CREDITO": rede_cartao_credito(str(entry["credenciadora"])),
                    "TIPO_VENCIMENTO_PARCELAS": params.tipo_vencimento_parcelas,
                    "DIA_INICIO_PERIODO_VENCIMENTO": params.dia_inicio_periodo_vencimento,
                    "DIAS_PARA_VENC_PRIMEIRA_PARC": params.dias_para_venc_primeira_parc,
                    "QTD_PARCELAS_DIA_FIXO_VENC": int(entry["parcelas"]),
                    "CREDENCIADORA_ID": int(params.credenciadora_id),
                    "UTILIZAR_EM_VENDAS_WEB": params.utilizar_em_vendas_web,
                    "FORMA_CALC_DIF_CARTAO_PARC": params.forma_calc_dif_cartao_parc,
                    "PERM_VINCULAR_CRT_AUT_CAIXA": params.perm_vincular_crt_aut_caixa,
                    "BANDEIRA_CARTAO": bandeira_cod(str(entry["bandeira"])),
                    "TIPO_PARCELAMENTO": params.tipo_parcelamento,
                    "TIPO_COBRANCA_RETENCAO": params.tipo_cobranca_retencao,
                    "TIPO_RETENCAO_CARTAO": tipo_retencao_cartao(str(entry["credenciadora"])),
                    "VENCIMENTO_PARC_PROX_DIA_UTIL": params.vencimento_parc_prox_dia_util,
                    "RECEBIMENTO_UNICO_PAG_SEGURO": params.recebimento_unico_pag_seguro,
                    "APENAS_DIAS_UTEIS_CALCULO_PRAZO": params.apenas_dias_uteis_calculo_prazo,
                    "TIPO_INICIO_PERIODO_VENCIMENTO": params.tipo_inicio_periodo_vencimento,
                    "TIPO_VENCIMENTO_PRIMEIRA_PARC": params.tipo_vencimento_primeira_parc,
                }
            )

            prazos_rows.append(
                {
                    "CHAVE_IMPORTACAO": chave,
                    "DIAS": int(entry["dias"]),
                }
            )

            for empresa_id in entry["empresas"]:
                retencoes_rows.append(
                    {
                        "CHAVE_IMPORTACAO": chave,
                        "EMPRESA_ID": int(empresa_id),
                        "TAXA_COBRANCA": entry["taxa"],
                        "NOVA_TAXA_COBRANCA": 0,
                        "DATA_NOVA_TAXA_COBRANCA": "",
                        "EMPRESA_USA_CARTAO": "S",
                    }
                )

    outputs = {
        "portadores.csv": portadores_df,
        "cartoes.csv": pd.DataFrame(cartoes_rows),
        "prazos.csv": pd.DataFrame(prazos_rows),
        "retencoes.csv": pd.DataFrame(retencoes_rows),
    }
    return outputs


def build_zip(outputs: Dict[str, pd.DataFrame]) -> bytes:
    memory = BytesIO()
    with zipfile.ZipFile(memory, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename, df in outputs.items():
            zf.writestr(filename, df.to_csv(index=False, sep=";", encoding="utf-8-sig"))
    return memory.getvalue()
