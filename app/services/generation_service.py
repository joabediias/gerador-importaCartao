from __future__ import annotations

from typing import Dict, List, Tuple

import pandas as pd

from app.domain.mappings import BANDEIRA_COD_MAP, BANDEIRA_TEF_MAP, REDE_CREDITO_MAP, TIPO_RETENCAO_MAP
from app.domain.models import AppParams, OutputBundle
from app.domain.validators import ValidationError
from app.services.excel_service import ExcelService
from app.utils.parsing import normalize_text, parse_empresas, parse_numeric


class GenerationService:
    @staticmethod
    def rede_cartao_tef(credenciadora: str) -> str:
        if credenciadora == "CIELO":
            return "CIELO"
        if credenciadora in {"REDE", "REDECARD"}:
            return "REDECARD"
        return "GETNET"

    @staticmethod
    def rede_cartao_credito(credenciadora: str) -> str:
        return REDE_CREDITO_MAP.get(credenciadora, "G")

    @staticmethod
    def tipo_retencao_cartao(credenciadora: str) -> str:
        return TIPO_RETENCAO_MAP.get(credenciadora, "G")

    @staticmethod
    def tipo_cartao(tipo: str) -> str:
        return "D" if tipo == "DEBITO" else "C"

    @staticmethod
    def bandeira_tef(bandeira: str) -> str:
        return BANDEIRA_TEF_MAP.get(bandeira, bandeira)

    @staticmethod
    def bandeira_cod(bandeira: str) -> str:
        return BANDEIRA_COD_MAP.get(bandeira, bandeira[:3])

    @staticmethod
    def build_nome_cartao(cred: str, bandeira: str, tipo: str, parcelas: int) -> str:
        suffix = f" {parcelas:02d}X" if tipo == "PARCELADO" else ""
        return f"{cred} - {bandeira} {tipo}{suffix}"

    @staticmethod
    def recebimento_variants(tipo_recebimento: str) -> List[str]:
        return ["POS", "TEF"] if tipo_recebimento == "AMBOS" else [tipo_recebimento]

    @classmethod
    def extract_rate_entries(cls, df: pd.DataFrame) -> List[Dict[str, object]]:
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
                entries.append({
                    "credenciadora": cred,
                    "bandeira": bandeira,
                    "tipo": "DEBITO",
                    "parcelas": 1,
                    "taxa": deb,
                    "dias": int(dias_debito) if str(dias_debito).strip() else 0,
                    "empresas": empresas,
                    "source_row": excel_row,
                })

            credit = parse_numeric(row.get("1X"))
            if credit is not None:
                entries.append({
                    "credenciadora": cred,
                    "bandeira": bandeira,
                    "tipo": "CREDITO",
                    "parcelas": 1,
                    "taxa": credit,
                    "dias": int(dias_credito) if str(dias_credito).strip() else 0,
                    "empresas": empresas,
                    "source_row": excel_row,
                })

            for parcela in range(2, 25):
                rate = parse_numeric(row.get(f"{parcela}X"))
                if rate is None:
                    continue
                entries.append({
                    "credenciadora": cred,
                    "bandeira": bandeira,
                    "tipo": "PARCELADO",
                    "parcelas": parcela,
                    "taxa": rate,
                    "dias": int(dias_parcelado) if str(dias_parcelado).strip() else 0,
                    "empresas": empresas,
                    "source_row": excel_row,
                })

        if not entries:
            raise ValidationError("Nenhuma taxa válida foi encontrada na aba TAXAS.")
        return entries

    @staticmethod
    def build_portadores(entries: List[Dict[str, object]]) -> Tuple[pd.DataFrame, Dict[Tuple[str, str, str], int]]:
        seen: Dict[Tuple[str, str, str], int] = {}
        rows = []
        next_id = 8000
        for entry in entries:
            key = (entry["credenciadora"], entry["bandeira"], entry["tipo"])
            if key in seen:
                continue
            seen[key] = next_id
            rows.append({
                "PORTADOR_ID": next_id,
                "NOME": f"{entry['bandeira']} {entry['tipo']} - {entry['credenciadora']}",
            })
            next_id += 1
        return pd.DataFrame(rows), seen

    @staticmethod
    def get_credenciadora_id(params: AppParams, credenciadora: str) -> int:
        cred_normalizada = normalize_text(credenciadora)

        credenciadora_id = params.credenciadora_ids.get(cred_normalizada)

        if credenciadora_id is None:
            raise ValidationError(
                f"Informe o código da credenciadora '{cred_normalizada}' antes de gerar os arquivos."
            )
        
        return int(credenciadora_id)

    @classmethod
    def build_outputs(cls, file_bytes: bytes, params: AppParams) -> OutputBundle:
        taxas_df = ExcelService.read_taxas(file_bytes)
        entries = cls.extract_rate_entries(taxas_df)
        portadores_df, portador_map = cls.build_portadores(entries)

        cartoes_rows = []
        prazos_rows = []
        retencoes_rows = []
        sequence = 1

        for entry in entries:
            for recebimento in cls.recebimento_variants(params.tipo_recebimento):
                chave = f"{entry['credenciadora']}{sequence}"
                sequence += 1
                portador_id = portador_map[(entry["credenciadora"], entry["bandeira"], entry["tipo"])]
                credenciadora_id = cls.get_credenciadora_id(
                    params,
                    str(entry["credenciadora"]),
                )
                cartoes_rows.append({
                    "CHAVE_IMPORTACAO": chave,
                    "NOME": cls.build_nome_cartao(entry["credenciadora"], entry["bandeira"], entry["tipo"], int(entry["parcelas"])),
                    "NUMERO_CONTRATO": "X",
                    "REDE_CARTAO_TEF": cls.rede_cartao_tef(str(entry["credenciadora"])),
                    "BANDEIRA_CARTAO_TEF": cls.bandeira_tef(str(entry["bandeira"])),
                    "PORTADOR_ID": portador_id,
                    "TIPO_CARTAO": cls.tipo_cartao(str(entry["tipo"])),
                    "TIPO_RECEBIMENTO": recebimento,
                    "ATIVO": "S",
                    "PARCELAS": int(entry["parcelas"]),
                    "AJUSTAR_PARC_CART_IMP_FISCAL": "S",
                    "LIBERADA_CONS_FINAL_PADRAO": params.liberada_cons_final_padrao,
                    "REDE_CARTAO_CREDITO": cls.rede_cartao_credito(str(entry["credenciadora"])),
                    "TIPO_VENCIMENTO_PARCELAS": params.tipo_vencimento_parcelas,
                    "DIA_INICIO_PERIODO_VENCIMENTO": params.dia_inicio_periodo_vencimento,
                    "DIAS_PARA_VENC_PRIMEIRA_PARC": params.dias_para_venc_primeira_parc,
                    "QTD_PARCELAS_DIA_FIXO_VENC": int(entry["parcelas"]),
                    "CREDENCIADORA_ID": credenciadora_id,
                    "UTILIZAR_EM_VENDAS_WEB": params.utilizar_em_vendas_web,
                    "FORMA_CALC_DIF_CARTAO_PARC": params.forma_calc_dif_cartao_parc,
                    "PERM_VINCULAR_CRT_AUT_CAIXA": params.perm_vincular_crt_aut_caixa,
                    "BANDEIRA_CARTAO": cls.bandeira_cod(str(entry["bandeira"])),
                    "TIPO_PARCELAMENTO": params.tipo_parcelamento,
                    "TIPO_COBRANCA_RETENCAO": params.tipo_cobranca_retencao,
                    "TIPO_RETENCAO_CARTAO": cls.tipo_retencao_cartao(str(entry["credenciadora"])),
                    "VENCIMENTO_PARC_PROX_DIA_UTIL": params.vencimento_parc_prox_dia_util,
                    "RECEBIMENTO_UNICO_PAG_SEGURO": params.recebimento_unico_pag_seguro,
                    "APENAS_DIAS_UTEIS_CALCULO_PRAZO": params.apenas_dias_uteis_calculo_prazo,
                    "TIPO_INICIO_PERIODO_VENCIMENTO": params.tipo_inicio_periodo_vencimento,
                    "TIPO_VENCIMENTO_PRIMEIRA_PARC": params.tipo_vencimento_primeira_parc,
                })

                prazos_rows.append({"CHAVE_IMPORTACAO": chave, "DIAS": int(entry["dias"])})

                for empresa_id in entry["empresas"]:
                    retencoes_rows.append({
                        "CHAVE_IMPORTACAO": chave,
                        "EMPRESA_ID": int(empresa_id),
                        "TAXA_COBRANCA": entry["taxa"],
                        "NOVA_TAXA_COBRANCA": 0,
                        "DATA_NOVA_TAXA_COBRANCA": "",
                        "EMPRESA_USA_CARTAO": "S",
                    })

        return OutputBundle(tables={
            "portadores.csv": portadores_df,
            "cartoes.csv": pd.DataFrame(cartoes_rows),
            "prazos.csv": pd.DataFrame(prazos_rows),
            "retencoes.csv": pd.DataFrame(retencoes_rows),
        })
