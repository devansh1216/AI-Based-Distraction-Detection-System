"""
Camera-related Pydantic schemas.
"""

from datetime import datetime

from pydantic import ConfigDict, Field

from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Base Schema
# ------------------------------------------------------------------------------


class CameraBase(BaseSchema):
    """
    Base schema shared across camera schemas.
    """

    classroom_id: int = Field(
        ...,
        gt=0,
    )

    camera_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Front Camera"],
    )

    camera_source: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["0", "rtsp://192.168.1.10/live"],
    )

    camera_type: str = Field(
        ...,
        min_length=2,
        max_length=30,
        examples=["USB"],
    )

    resolution: str | None = Field(
        default=None,
        max_length=20,
        examples=["1920x1080"],
    )

    fps: int | None = Field(
        default=None,
        ge=1,
        le=240,
    )

    is_active: bool = True


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class CameraCreate(CameraBase):
    """
    Schema used when registering a new camera.
    """

    pass


# ------------------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------------------


class CameraUpdate(BaseSchema):
    """
    Schema used for updating camera information.

    All fields are optional.
    """

    classroom_id: int | None = Field(
        default=None,
        gt=0,
    )

    camera_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    camera_source: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    camera_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=30,
    )

    resolution: str | None = Field(
        default=None,
        max_length=20,
    )

    fps: int | None = Field(
        default=None,
        ge=1,
        le=240,
    )

    is_active: bool | None = None


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class CameraResponse(CameraBase):
    """
    Camera information returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime

    updated_at: datetime


# ------------------------------------------------------------------------------
# Summary Schema
# ------------------------------------------------------------------------------


class CameraSummary(BaseSchema):
    """
    Lightweight camera information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    classroom_id: int

    camera_name: str

    camera_type: str

    is_active: bool