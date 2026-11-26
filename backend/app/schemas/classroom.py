"""
Classroom-related Pydantic schemas.
"""

from datetime import datetime

from pydantic import ConfigDict, Field

from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Base Schema
# ------------------------------------------------------------------------------


class ClassroomBase(BaseSchema):
    """
    Base schema shared across classroom schemas.
    """

    classroom_code: str = Field(
        ...,
        min_length=1,
        max_length=20,
        examples=["CSE-101"],
    )

    classroom_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Computer Science Lab"],
    )

    floor_number: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    building_name: str | None = Field(
        default=None,
        max_length=100,
        examples=["Engineering Block"],
    )

    max_capacity: int = Field(
        ...,
        ge=1,
        le=500,
        examples=[60],
    )

    is_active: bool = True


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class ClassroomCreate(ClassroomBase):
    """
    Schema used when creating a classroom.
    """

    pass


# ------------------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------------------


class ClassroomUpdate(BaseSchema):
    """
    Schema used for updating classroom information.

    All fields are optional.
    """

    classroom_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    classroom_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    floor_number: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    building_name: str | None = Field(
        default=None,
        max_length=100,
    )

    max_capacity: int | None = Field(
        default=None,
        ge=1,
        le=500,
    )

    is_active: bool | None = None


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class ClassroomResponse(ClassroomBase):
    """
    Classroom information returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime

    updated_at: datetime


# ------------------------------------------------------------------------------
# Summary Schema
# ------------------------------------------------------------------------------


class ClassroomSummary(BaseSchema):
    """
    Lightweight classroom information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    classroom_code: str

    classroom_name: str