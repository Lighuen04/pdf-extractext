"""Infrastructure models (MongoDB document schemas)."""

from datetime import datetime
from typing import Any, Optional
from bson import ObjectId


class DocumentModel:
    """MongoDB model for PDF documents."""

    COLLECTION_NAME = "documents"

    @staticmethod
    def create_schema() -> dict[str, Any]:
        """Return MongoDB schema/template for a document."""
        return {
            "_id": ObjectId(),
            "filename": str,
            "original_filename": str,
            "file_size": int,
            "file_path": str,
            "mime_type": str,
            "status": str,  # pending, processing, completed, failed
            "created_at": datetime,
            "updated_at": datetime,
            "uploaded_by": Optional[str],
            "error_message": Optional[str],
            "metadata": dict,  # Additional metadata
        }

    @staticmethod
    def to_dict(doc: dict[str, Any]) -> dict[str, Any]:
        """Convert MongoDB document to dictionary for API responses."""
        return {
            "id": str(doc.get("_id", "")),
            "filename": doc.get("filename", ""),
            "original_filename": doc.get("original_filename", ""),
            "file_size": doc.get("file_size", 0),
            "status": doc.get("status", ""),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
            "error_message": doc.get("error_message"),
        }
