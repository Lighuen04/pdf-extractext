"""Compatibility wrapper for ``src.application`` imports."""

from application import (
    DocumentDTO,
    DocumentService,
    ExtractTextUseCase,
    ExtractionResultDTO,
    ExtractionService,
    SummarizationResultDTO,
    SummarizationService,
    SummarizeTextUseCase,
    UploadDocumentUseCase,
)

__all__ = [
    "DocumentDTO",
    "DocumentService",
    "ExtractTextUseCase",
    "ExtractionResultDTO",
    "ExtractionService",
    "SummarizationResultDTO",
    "SummarizationService",
    "SummarizeTextUseCase",
    "UploadDocumentUseCase",
]
