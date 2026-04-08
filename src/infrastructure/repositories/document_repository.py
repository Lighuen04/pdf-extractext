from datetime import datetime
from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase as AsyncDatabase

from .base_repository import BaseRepository
from src.infrastructure.models import DocumentModel


class DocumentRepository(BaseRepository):
    """Repository for managing PDF documents in MongoDB."""

    def __init__(self, database: AsyncDatabase):
        super().__init__(database, DocumentModel.COLLECTION_NAME)

    async def create_document(
        self,
        filename: str,
        original_filename: str,
        file_size: int,
        file_path: str,
        mime_type: str = "application/pdf",
        uploaded_by: Optional[str] = None,
    ) -> str:
        doc = {
            "filename": filename,
            "original_filename": original_filename,
            "file_size": file_size,
            "file_path": file_path,
            "mime_type": mime_type,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "uploaded_by": uploaded_by,
            "error_message": None,
            "metadata": {},
        }
        return await self.create(doc)

    async def get_document_by_id(self, document_id: str) -> Optional[dict[str, Any]]:
        return await self.read_by_id(document_id)

    async def get_documents_by_status(
        self, status: str, skip: int = 0, limit: int = 10
    ) -> list[dict[str, Any]]:
        cursor = self.collection.find({"status": status}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def update_document_status(
        self, document_id: str, status: str, error_message: Optional[str] = None
    ) -> bool:
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow(),
        }
        if error_message:
            update_data["error_message"] = error_message

        result = await self.collection.update_one(
            {"id": document_id},
            {"$set": update_data},
        )
        return result.modified_count > 0

    async def count_documents_by_status(self, status: str) -> int:
        return await self.collection.count_documents({"status": status})