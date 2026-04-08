"""Compatibility wrapper for ``src.infrastructure`` imports."""

from infrastructure import (
    AISummarizerAdapter,
    BaseRepository,
    DocumentModel,
    DocumentRepository,
    MongoDBAdapter,
    MongoDBConnection,
    PDFExtractorAdapter,
    connect_database,
    disconnect_database,
    get_database,
)

__all__ = [
    "AISummarizerAdapter",
    "BaseRepository",
    "DocumentModel",
    "DocumentRepository",
    "MongoDBAdapter",
    "MongoDBConnection",
    "PDFExtractorAdapter",
    "connect_database",
    "disconnect_database",
    "get_database",
]

