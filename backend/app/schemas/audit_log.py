"""
Audit Log related Pydantic schemas.
"""

from datetime import datetime

from pydantic import ConfigDict, Field

from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Base Schema
# ------------------------------------------------------------------------------


class AuditLogBase(BaseSchema):
    """
    Base schema shared across audit log schemas.
    """

    user_id: int = Field(
        ...,
        gt=0,
    )

    action_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        examples=["LOGIN"],
    )

    action_description: str | None = Field(
        default=None,
    )

    ip_address: str | None = Field(
        default=None,
        max_length=45,
        examples=["192.168.1.100"],
    )


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class AuditLogCreate(AuditLogBase):
    """
    Schema used internally when creating audit logs.
    """

    pass


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class AuditLogResponse(AuditLogBase):
    """
    Audit log returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime


# ------------------------------------------------------------------------------
# Summary Schema
# ------------------------------------------------------------------------------


class AuditLogSummary(BaseSchema):
    """
    Lightweight audit log information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    user_id: int

    action_type: str

    created_at: datetime