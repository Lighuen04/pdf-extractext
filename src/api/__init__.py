"""API module initialization."""

from .schemas import (
    DocumentCreateRequest,
    DocumentResponse,
    DocumentListResponse,
    ExtractionRequest,
    ExtractionResponse,
    SummarizationRequest,
    SummarizationResponse,
    HealthCheckResponse,
)
from .dependencies import DIContainer, get_di_container

__all__ = [
    # Schemas
    "DocumentCreateRequest",
    "DocumentResponse",
    "DocumentListResponse",
    "ExtractionRequest",
    "ExtractionResponse",
    "SummarizationRequest",
    "SummarizationResponse",
    "HealthCheckResponse",
    # Dependencies
    "DIContainer",
    "get_di_container",
]
