from __future__ import annotations

from io import BytesIO
import pandas as pd

from app.domain.validators import ensure_columns, ensure_not_empty, ValidationError


class ExcelService:
    @staticmethod
    def read_taxas(file_bytes: bytes) -> pd.DataFrame:
        try:
            df = pd.read_excel(BytesIO(file_bytes), sheet_name="TAXAS", header=3)
        except Exception as exc:
            raise ValidationError(f"Não foi possível ler a aba TAXAS: {exc}") from exc

        ensure_columns(df)
        df = df.fillna("")
        df = df[df["EMPRESAS"].astype(str).str.strip() != ""].copy()
        ensure_not_empty(df)
        return df
