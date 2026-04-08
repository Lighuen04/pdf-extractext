"""Pytest configuration and fixtures."""

import pytest
import asyncio
from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from unittest.mock import AsyncMock

from main import create_app, app
from src.config import Settings


# Configure pytest for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def settings() -> Settings:
    """Provide test settings."""
    return Settings(
        DEBUG=True,
        MONGODB_URL="mongodb://localhost:27017",
        MONGODB_DATABASE="pdf_extractext_test",
    )


@pytest.fixture
async def mock_database() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Provide a mock MongoDB database for testing."""
    # Create a mock database
    mock_db = AsyncMock(spec=AsyncIOMotorDatabase)
    mock_db.command = AsyncMock(return_value={"ok": 1})
    yield mock_db


@pytest.fixture
async def test_app():
    """Provide a test FastAPI application instance."""
    test_settings = Settings(
        DEBUG=True,
        MONGODB_URL="mongodb://localhost:27017",
        MONGODB_DATABASE="pdf_extractext_test",
    )
    return create_app(test_settings)


@pytest.fixture
def test_client():
    """Provide a test client for API testing."""
    from fastapi.testclient import TestClient
    
    return TestClient(app)
