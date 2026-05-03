from __future__ import annotations

from io import BytesIO
from time import perf_counter
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.repositories.document_repository import DocumentRepository
from app.services.checksum_service import calc_checksum
from app.services.document_builder import construir_documento


class InvalidPDFError(ValueError):
    pass


def process_pdf_upload(
    *,
    file_name: str,
    file_bytes: bytes,
    repository: DocumentRepository | None = None,
) -> dict[str, Any]:
    started_at = perf_counter()
    extracted_text = extract_text_from_pdf_bytes(file_bytes)
    checksum = calc_checksum(file_bytes)
    duration_ms = int((perf_counter() - started_at) * 1000)

    document = construir_documento(
        pdf_nombre=file_name,
        texto_extraido=extracted_text,
        checksum_archivo=checksum,
        duracion_ms=duration_ms,
    )

    active_repository = repository or DocumentRepository()
    inserted_id = active_repository.save_document(document)

    return {
        "document_id": str(inserted_id),
        "document": document,
    }


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    if not file_bytes.startswith(b"%PDF-"):
        raise InvalidPDFError("El contenido no corresponde a un PDF valido.")

    try:
        reader = PdfReader(BytesIO(file_bytes))
    except (PdfReadError, ValueError) as exc:
        raise InvalidPDFError("El contenido no corresponde a un PDF valido.") from exc

    pages_text = [(page.extract_text() or "").strip() for page in reader.pages]
    return "\n".join(text for text in pages_text if text).strip()

