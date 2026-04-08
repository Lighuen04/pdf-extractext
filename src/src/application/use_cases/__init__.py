"""Compatibility wrapper for ``src.application.use_cases`` imports."""

from application.use_cases import (
    ExtractTextUseCase,
    SummarizeTextUseCase,
    UploadDocumentUseCase,
)

__all__ = [
    "ExtractTextUseCase",
    "SummarizeTextUseCase",
    "UploadDocumentUseCase",
]
