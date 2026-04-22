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
