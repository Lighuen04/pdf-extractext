"""Database connection module."""

from typing import Optional

from motor.motor_asyncio import (
    AsyncIOMotorClient as AsyncClient,
    AsyncIOMotorDatabase as AsyncDatabase,
)
from src.config import get_settings


class MongoDBConnection:
    """Singleton class for MongoDB connection management."""

    _instance = None
    _client: Optional[AsyncClient] = None
    _database: Optional[AsyncDatabase] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self) -> None:
        """Establish MongoDB connection."""
        settings = get_settings()
        self._client = AsyncClient(
            settings.MONGODB_URL, serverSelectionTimeoutMS=settings.MONGODB_TIMEOUT
        )
        self._database = self._client[settings.MONGODB_DATABASE]
        # Verify connection
        await self._database.command("ping")
        print(f"Connected to MongoDB: {settings.MONGODB_DATABASE}")

    async def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            print("Disconnected from MongoDB")

    @property
    def database(self) -> AsyncDatabase:
        """Get the MongoDB database instance."""
        if self._database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._database

    @property
    def client(self) -> AsyncClient:
        """Get the MongoDB client instance."""
        if self._client is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._client


# Global instance
_db_connection = MongoDBConnection()


async def get_database() -> AsyncDatabase:
    """Dependency injection function for database access."""
    return _db_connection.database


async def connect_database() -> None:
    """Connect to the database on startup."""
    await _db_connection.connect()


async def disconnect_database() -> None:
    """Disconnect from the database on shutdown."""
    await _db_connection.disconnect()
