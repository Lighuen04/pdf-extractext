"""MongoDB adapter for database operations."""

from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase as AsyncDatabase


class MongoDBAdapter:
    """Adapter for MongoDB database operations.
    
    Provides a higher-level interface for common database operations.
    """

    def __init__(self, database: AsyncDatabase):
        self.database = database

    async def health_check(self) -> bool:
        """Check if database connection is healthy."""
        try:
            await self.database.command("ping")
            return True
        except Exception:
            return False

    async def get_collection_stats(self, collection_name: str) -> dict[str, Any]:
        """Get statistics for a collection."""
        try:
            stats = await self.database.command("collStats", collection_name)
            return stats
        except Exception:
            return {}
