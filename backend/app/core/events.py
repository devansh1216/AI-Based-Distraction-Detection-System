from fastapi import FastAPI

from app.db.base import Base
from app.core.database import engine


def register_startup_event(app: FastAPI) -> None:
    """
    Register application startup event.

    Infrastructure only.
    Business logic, database initialization,
    background tasks, and external services
    will be added in future implementation steps.
    """

    @app.on_event("startup")
    async def startup() -> None:
        Base.metadata.create_all(bind=engine)


def register_shutdown_event(app: FastAPI) -> None:
    """
    Register application shutdown event.

    Cleanup logic will be implemented
    in later phases.
    """

    @app.on_event("shutdown")
    async def shutdown() -> None:
        pass