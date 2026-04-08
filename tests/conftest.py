import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorDatabase

import main
import src.infrastructure.database.connection as connection
from main import create_app
from src.config import Settings
from src.infrastructure import get_database


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def settings() -> Settings:
    return Settings(
        DEBUG=True,
        MONGODB_URL="mongodb://localhost:27017",
        MONGODB_DATABASE="pdf_extractext_test",
    )


@pytest.fixture
def mock_database() -> AsyncIOMotorDatabase:
    mock_db = MagicMock(spec=AsyncIOMotorDatabase)

    mock_collection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.to_list = AsyncMock(return_value=[])
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor

    mock_collection.find.return_value = mock_cursor
    mock_db.__getitem__.return_value = mock_collection
    mock_db.command = AsyncMock(return_value={"ok": 1})

    return mock_db


@pytest.fixture
def test_app(settings, mock_database, monkeypatch):
    monkeypatch.setattr(main, "connect_database", AsyncMock(return_value=None))
    monkeypatch.setattr(main, "disconnect_database", AsyncMock(return_value=None))

    app = create_app(settings)

    app.dependency_overrides[get_database] = lambda: mock_database
    app.dependency_overrides[connection.get_database] = lambda: mock_database

    return app


@pytest.fixture
def test_client(test_app):
    with TestClient(test_app) as client:
        yield client
