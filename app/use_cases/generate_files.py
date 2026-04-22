from __future__ import annotations

from pathlib import Path

from app.domain.models import AppParams, GenerationResult
from app.services.export_service import ExportService
from app.services.generation_service import GenerationService


def generate_import_files(file_path: Path, params: AppParams) -> GenerationResult:
    file_bytes = file_path.read_bytes()
    bundle = GenerationService.build_outputs(file_bytes, params)
    bundle.zip_bytes = ExportService.build_zip(bundle)
    return GenerationResult(
        bundle=bundle,
        source_file=file_path,
        messages=["Arquivos gerados com sucesso."],
    )
