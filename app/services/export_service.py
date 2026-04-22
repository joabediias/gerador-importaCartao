from __future__ import annotations

from io import BytesIO
from pathlib import Path
import zipfile

from app.domain.constants import CSV_ENCODING, CSV_SEPARATOR
from app.domain.models import OutputBundle


class ExportService:
    @staticmethod
    def build_zip(bundle: OutputBundle) -> bytes:
        memory = BytesIO()
        with zipfile.ZipFile(memory, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for filename, df in bundle.tables.items():
                zf.writestr(filename, df.to_csv(index=False, sep=CSV_SEPARATOR, encoding=CSV_ENCODING))
        return memory.getvalue()

    @staticmethod
    def save_csvs(bundle: OutputBundle, destination_dir: Path) -> None:
        destination_dir.mkdir(parents=True, exist_ok=True)
        for filename, df in bundle.tables.items():
            df.to_csv(destination_dir / filename, index=False, sep=CSV_SEPARATOR, encoding=CSV_ENCODING)

    @staticmethod
    def save_zip_file(zip_bytes: bytes, destination: Path) -> None:
        destination.write_bytes(zip_bytes)
