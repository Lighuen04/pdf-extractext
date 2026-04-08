"""Compatibility wrapper for ``src.api.schemas`` imports."""

from api.schemas import (
    DocumentCreateRequest,
    DocumentListResponse,
    DocumentResponse,
    ExtractionRequest,
    ExtractionResponse,
    HealthCheckResponse,
    SummarizationRequest,
    SummarizationResponse,
)

__all__ = [
    "DocumentCreateRequest",
    "DocumentListResponse",
    "DocumentResponse",
    "ExtractionRequest",
    "ExtractionResponse",
    "HealthCheckResponse",
    "SummarizationRequest",
    "SummarizationResponse",
]
