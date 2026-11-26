"""
Authentication-related Pydantic schemas.
"""

from pydantic import ConfigDict, EmailStr, Field

from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Login Request
# ------------------------------------------------------------------------------


class LoginRequest(BaseSchema):
    """
    Schema for user login requests.
    """

    email: EmailStr = Field(
        ...,
        description="Registered email address",
        examples=["teacher@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
        examples=["StrongPassword123"],
    )


# ------------------------------------------------------------------------------
# JWT Token Response
# ------------------------------------------------------------------------------


class Token(BaseSchema):
    """
    JWT access token returned after successful authentication.
    """

    access_token: str

    token_type: str = "bearer"


# ------------------------------------------------------------------------------
# JWT Payload
# ------------------------------------------------------------------------------


class TokenPayload(BaseSchema):
    """
    JWT payload after successful decoding.

    This schema is used internally by the authentication
    layer and does not perform token verification.
    """

    sub: str


# ------------------------------------------------------------------------------
# Change Password
# ------------------------------------------------------------------------------


class ChangePasswordRequest(BaseSchema):
    """
    Schema for changing the authenticated user's password.
    """

    current_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


# ------------------------------------------------------------------------------
# Refresh Token
# ------------------------------------------------------------------------------


class RefreshTokenRequest(BaseSchema):
    """
    Placeholder schema for future refresh-token support.

    Version 1 currently uses only access tokens,
    but this schema keeps the API extensible.
    """

    refresh_token: str


# ------------------------------------------------------------------------------
# Authenticated User
# ------------------------------------------------------------------------------


class AuthenticatedUser(BaseSchema):
    """
    Minimal authenticated user information
    extracted from the authenticated database user.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    email: EmailStr

    role: str