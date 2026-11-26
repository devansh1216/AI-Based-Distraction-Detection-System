from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.api import api_router
from app.core.events import (
    register_shutdown_event,
    register_startup_event,
)
from app.exceptions.handlers import register_exception_handlers

# ------------------------------------------------------------------------------
# FastAPI Application
# ------------------------------------------------------------------------------

app = FastAPI(
    title="AI-Based Classroom Distraction Detection System API",
    description="Backend REST API for the AI-Based Classroom Distraction Detection System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
)

# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Application Lifecycle Events
# ------------------------------------------------------------------------------

register_startup_event(app)
register_shutdown_event(app)
register_exception_handlers(app)

# ------------------------------------------------------------------------------
# API Versioning
# ------------------------------------------------------------------------------

app.include_router(api_router, prefix="/api/v1")

# ------------------------------------------------------------------------------
# Health Check
# ------------------------------------------------------------------------------

@app.get(
    "/health",
    tags=["Infrastructure"],
    summary="Application Health Check",
)
async def health_check():
    """
    Health check endpoint used to verify that the backend server
    is running and accepting requests.
    """
    return {
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0",
    }


frontend_directory = Path(__file__).resolve().parents[2] / "frontend"
app.mount(
    "/",
    StaticFiles(directory=frontend_directory, html=True),
    name="frontend",
)