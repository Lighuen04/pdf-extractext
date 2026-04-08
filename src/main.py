from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.config.settings import Settings
from src.infrastructure.database.connection import connect_database, disconnect_database

from src.api.routes import health, documents


def create_app(settings: Settings) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await connect_database()
        yield
        await disconnect_database()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    # Routers
    app.include_router(health.router)
    app.include_router(documents.router, prefix="/api/v1")

    return app