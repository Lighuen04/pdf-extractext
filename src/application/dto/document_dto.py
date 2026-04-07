"""Data Transfer Objects for document operations."""

from datetime import datetime
from typing import Optional


class DocumentDTO:
    """DTO for document data transfer."""

    def __init__(
        self,
        id: str,
        filename: str,
        original_filename: str,
        file_size: int,
        status: str,
        created_at: datetime,
        updated_at: datetime,
        error_message: Optional[str] = None,
    ):
        self.id = id
        self.filename = filename
        self.original_filename = original_filename
        self.file_size = file_size
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.error_message = error_message

    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_size": self.file_size,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "error_message": self.error_message,
        }


class ExtractionResultDTO:
    """DTO for PDF text extraction results."""

    def __init__(
        self,
        document_id: str,
        extracted_text: str,
        page_count: int,
        extraction_time_ms: float,
    ):
        self.document_id = document_id
        self.extracted_text = extracted_text
        self.page_count = page_count
        self.extraction_time_ms = extraction_time_ms

    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            "document_id": self.document_id,
            "extracted_text": self.extracted_text,
            "page_count": self.page_count,
            "extraction_time_ms": self.extraction_time_ms,
        }


class SummarizationResultDTO:
    """DTO for text summarization results."""

    def __init__(
        self,
        document_id: str,
        original_text: str,
        summary: str,
        keywords: list[str],
        summarization_time_ms: float,
    ):
        self.document_id = document_id
        self.original_text = original_text
        self.summary = summary
        self.keywords = keywords
        self.summarization_time_ms = summarization_time_ms

    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            "document_id": self.document_id,
            "original_text": self.original_text,
            "summary": self.summary,
            "keywords": self.keywords,
            "summarization_time_ms": self.summarization_time_ms,
        }
