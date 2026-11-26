"""
Common Pydantic schemas shared across the application.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base schema for all response models.

    Enables serialization from SQLAlchemy ORM objects.
    """

    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseSchema):
    """
    Shared timestamp fields used by multiple response schemas.
    """

    created_at: datetime


class TimestampUpdateSchema(TimestampSchema):
    """
    Shared timestamp fields for entities that maintain
    both creation and update timestamps.
    """

    updated_at: datetime


class MessageResponse(BaseModel):
    """
    Generic message response.
    """

    message: str


class HealthResponse(BaseModel):
    """
    Response model for the health check endpoint.
    """

    status: str
    service: str
    version: str