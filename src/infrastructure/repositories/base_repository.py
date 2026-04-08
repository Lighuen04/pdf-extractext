"""Base repository for common CRUD operations."""

from typing import Any, Generic, Optional, TypeVar
from motor.motor_asyncio import AsyncIOMotorDatabase as AsyncDatabase
from bson import ObjectId


T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic base repository for MongoDB operations."""

    def __init__(self, database: AsyncDatabase, collection_name: str):
        self.database = database
        self.collection_name = collection_name
        self.collection = database[collection_name]

    async def create(self, data: dict[str, Any]) -> str:
        """Create a new document and return its ID."""
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def read_by_id(self, document_id: str) -> Optional[dict[str, Any]]:
        """Read a document by ID."""
        try:
            result = await self.collection.find_one({"_id": ObjectId(document_id)})
            return result
        except Exception:
            return None

    async def read_all(self, skip: int = 0, limit: int = 10) -> list[dict[str, Any]]:
        """Read all documents with pagination."""
        cursor = self.collection.find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def update(self, document_id: str, data: dict[str, Any]) -> bool:
        """Update a document."""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(document_id)}, {"$set": data}
            )
            return result.modified_count > 0
        except Exception:
            return False

    async def delete(self, document_id: str) -> bool:
        """Delete a document."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def count(self) -> int:
        """Count documents in collection."""
        return await self.collection.count_documents({})
