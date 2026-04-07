"""
FastAPI Application Entry Point.

Production-oriented FastAPI application for PDF text extraction and AI summarization
using a 3-layer enterprise architecture (API, Application, Infrastructure layers).
"""

import uvicorn
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings, Settings
from src.infrastructure import connect_database, disconnect_database
from src.api.routes import health, documents


# Application startup and shutdown lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    print("Starting up PDF Extractext application...")
    await connect_database()
    print("Database connected successfully")
    
    yield
    
    # Shutdown
    print("Shutting down PDF Extractext application...")
    await disconnect_database()
    print("Database disconnected successfully")


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Args:
        settings: Application settings (uses defaults if None)
        
    Returns:
        Configured FastAPI application instance
    """
    if settings is None:
        settings = get_settings()
    
    # Initialize FastAPI app with lifespan manager
    app = FastAPI(
        title=settings.APP_NAME,
        description="API for PDF text extraction and AI summarization",
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(documents.router, prefix=settings.API_PREFIX)
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint - welcome message."""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "status": "running",
            "docs_url": "/docs",
            "openapi_url": "/openapi.json",
        }
    
    return app


# Create the FastAPI application instance
app = create_app()


def main():
    """Run the FastAPI application."""
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )


if __name__ == "__main__":
    main()
