"""Adapters module initialization."""

from .mongodb_adapter import MongoDBAdapter
from .pdf_extractor_adapter import PDFExtractorAdapter
from .ai_summarizer_adapter import AISummarizerAdapter

__all__ = [
    "MongoDBAdapter",
    "PDFExtractorAdapter",
    "AISummarizerAdapter",
]
