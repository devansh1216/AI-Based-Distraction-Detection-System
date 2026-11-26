import logging
logger = logging.getLogger(__name__)
"""
Global exception handlers.
"""

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions.custom_exceptions import AppException


# ------------------------------------------------------------------------------
# Custom Exceptions
# ------------------------------------------------------------------------------


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    """
    Handle all custom application exceptions.
    """

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": exc.message,
        },
    )


# ------------------------------------------------------------------------------
# FastAPI HTTP Exceptions
# ------------------------------------------------------------------------------


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    """
    Handle FastAPI HTTP exceptions.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


# ------------------------------------------------------------------------------
# Request Validation Exceptions
# ------------------------------------------------------------------------------


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Handle request validation errors.
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Request validation failed.",
            "errors": exc.errors(),
        },
    )


# ------------------------------------------------------------------------------
# Database Exceptions
# ------------------------------------------------------------------------------


async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    """
    Handle SQLAlchemy database exceptions.
    """

    logger.error(
        "Database error on %s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "A database error occurred.",
        },
    )


# ------------------------------------------------------------------------------
# Unexpected Exceptions
# ------------------------------------------------------------------------------


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected server errors.
    """

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected error occurred.",
        },
    )


# ------------------------------------------------------------------------------
# Register Exception Handlers
# ------------------------------------------------------------------------------


def register_exception_handlers(
    app: FastAPI,
):
    """
    Register all global exception handlers.
    """

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        SQLAlchemyError,
        database_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        global_exception_handler,
    )