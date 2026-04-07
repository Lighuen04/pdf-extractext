"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Document Schemas
class DocumentCreateRequest(BaseModel):
    """Request schema for creating a document."""

    filename: str = Field(..., min_length=1, max_length=255)
    original_filename: str = Field(..., min_length=1, max_length=255)
    file_size: int = Field(..., gt=0)
    file_path: str = Field(..., min_length=1)


class DocumentResponse(BaseModel):
    """Response schema for document."""

    id: str
    filename: str
    original_filename: str
    file_size: int
    status: str
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Response schema for document list."""

    total: int
    skip: int
    limit: int
    documents: list[DocumentResponse]


# Extraction Schemas
class ExtractionRequest(BaseModel):
    """Request schema for text extraction."""

    document_id: str = Field(..., min_length=1)


class ExtractionResponse(BaseModel):
    """Response schema for text extraction."""

    document_id: str
    extracted_text: str
    page_count: int
    extraction_time_ms: float

    class Config:
        from_attributes = True


# Summarization Schemas
class SummarizationRequest(BaseModel):
    """Request schema for text summarization."""

    document_id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    max_length: Optional[int] = None


class SummarizationResponse(BaseModel):
    """Response schema for text summarization."""

    document_id: str
    summary: str
    keywords: list[str]
    summarization_time_ms: float

    class Config:
        from_attributes = True


# Health Check Schemas
class HealthCheckResponse(BaseModel):
    """Response schema for health check."""

    status: str
    message: str
    version: str
    database_connected: bool
