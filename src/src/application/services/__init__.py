"""Compatibility wrapper for ``src.application.services`` imports."""

from application.services import DocumentService, ExtractionService, SummarizationService

__all__ = [
    "DocumentService",
    "ExtractionService",
    "SummarizationService",
]

