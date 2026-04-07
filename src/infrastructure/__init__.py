"""Infrastructure module initialization."""

from .database import (
    MongoDBConnection,
    connect_database,
    disconnect_database,
    get_database,
)
from .models import DocumentModel
from .repositories import BaseRepository, DocumentRepository
from .adapters import (
    MongoDBAdapter,
    PDFExtractorAdapter,
    AISummarizerAdapter,
)

__all__ = [
    # Database
    "MongoDBConnection",
    "connect_database",
    "disconnect_database",
    "get_database",
    # Models
    "DocumentModel",
    # Repositories
    "BaseRepository",
    "DocumentRepository",
    # Adapters
    "MongoDBAdapter",
    "PDFExtractorAdapter",
    "AISummarizerAdapter",
]
