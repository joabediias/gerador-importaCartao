from __future__ import annotations

import re
from typing import List

import pandas as pd

from app.domain.validators import ValidationError


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
