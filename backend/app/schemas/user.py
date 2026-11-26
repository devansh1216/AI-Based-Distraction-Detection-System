"""
User-related Pydantic schemas.
"""

from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field

from app.schemas.common import BaseSchema

from app.enums.user import UserRole


# ------------------------------------------------------------------------------
# Base Schema
# ------------------------------------------------------------------------------


class UserBase(BaseSchema):
    """
    Base schema shared across user schemas.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["John Doe"],
    )

    email: EmailStr = Field(
        ...,
        examples=["john.doe@example.com"],
    )

    role: UserRole

    is_active: bool = True


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class UserCreate(UserBase):
    """
    Schema used when creating a new user.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["StrongPassword123"],
    )


# ------------------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------------------


class UserUpdate(BaseSchema):
    """
    Schema used for updating user information.

    All fields are optional.
    """

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: EmailStr | None = Field(
        default=None,
    )

    role: UserRole | None = None

    is_active: bool | None = None


# ------------------------------------------------------------------------------
# Status Update
# ------------------------------------------------------------------------------


class UserStatusUpdate(BaseSchema):
    """
    Enable or disable a user account.
    """

    is_active: bool


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class UserResponse(UserBase):
    """
    User information returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    last_login_at: datetime | None

    created_at: datetime

    updated_at: datetime


# ------------------------------------------------------------------------------
# Public User Schema
# ------------------------------------------------------------------------------


class UserPublic(BaseSchema):
    """
    Public user information.

    Does not expose account status or timestamps.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    full_name: str

    role: UserRole


# ------------------------------------------------------------------------------
# List Response
# ------------------------------------------------------------------------------


class UserListResponse(BaseSchema):
    """
    Wrapper schema for returning multiple users.
    """

    users: list[UserResponse]

    total: int