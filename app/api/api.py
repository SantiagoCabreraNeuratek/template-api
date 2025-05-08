"""
API router configuration module.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints import health, workflows


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        debug=settings.DEBUG,
    )

    # Set CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, you should specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix=settings.API_V1_STR)
    app.include_router(workflows.router, prefix=settings.API_V1_STR)

    return app 