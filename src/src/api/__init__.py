"""Compatibility wrapper for ``src.api`` imports."""

from api import (
    DIContainer,
    DocumentCreateRequest,
    DocumentListResponse,
    DocumentResponse,
    ExtractionRequest,
    ExtractionResponse,
    HealthCheckResponse,
    SummarizationRequest,
    SummarizationResponse,
    get_di_container,
)

__all__ = [
    "DIContainer",
    "DocumentCreateRequest",
    "DocumentListResponse",
    "DocumentResponse",
    "ExtractionRequest",
    "ExtractionResponse",
    "HealthCheckResponse",
    "SummarizationRequest",
    "SummarizationResponse",
    "get_di_container",
]

