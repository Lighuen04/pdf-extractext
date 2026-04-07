"""Health check router."""

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase as AsyncDatabase

from src.api.schemas import HealthCheckResponse
from src.config import get_settings, Settings
from src.infrastructure import get_database, MongoDBAdapter

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(
    settings: Settings = Depends(get_settings),
    database: AsyncDatabase = Depends(get_database),
) -> HealthCheckResponse:
    """Health check endpoint.
    
    Returns the status of the application and database connectivity.
    """
    # Check database connection
    db_adapter = MongoDBAdapter(database)
    db_connected = await db_adapter.health_check()

    return HealthCheckResponse(
        status="healthy" if db_connected else "unhealthy",
        message="Application is running",
        version=settings.APP_VERSION,
        database_connected=db_connected,
    )
