from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List
import pandas as pd


@dataclass(slots=True)
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


@dataclass(slots=True)
class OutputBundle:
    tables: Dict[str, pd.DataFrame]
    zip_bytes: bytes | None = None

    def counts(self) -> Dict[str, int]:
        return {name: len(df) for name, df in self.tables.items()}


@dataclass(slots=True)
class GenerationResult:
    bundle: OutputBundle
    source_file: Path | None = None
    messages: List[str] = field(default_factory=list)
