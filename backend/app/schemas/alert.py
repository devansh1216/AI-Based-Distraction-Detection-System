"""
Alert-related Pydantic schemas.
"""

from datetime import datetime
from app.enums.alert import (
    AlertSeverity,
    AlertStatus,
    AlertType,
)

from pydantic import ConfigDict, Field

from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Base Schema
# ------------------------------------------------------------------------------


class AlertBase(BaseSchema):
    """
    Base schema shared across alert schemas.
    """

    session_id: int = Field(..., gt=0)

    tracking_id: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    alert_type: AlertType

    severity: AlertSeverity

    status: AlertStatus = AlertStatus.ACTIVE

    generated_at: datetime

    acknowledged_at: datetime | None = None


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class AlertCreate(AlertBase):
    """
    Schema used internally when generating alerts.
    """

    pass


# ------------------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------------------


class AlertUpdate(BaseSchema):
    """
    Schema used for acknowledging or dismissing alerts.
    """

    status: AlertStatus

    acknowledged_at: datetime | None = None


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class AlertResponse(AlertBase):
    """
    Alert returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime


# ------------------------------------------------------------------------------
# Summary Schema
# ------------------------------------------------------------------------------


class AlertSummary(BaseSchema):
    """
    Lightweight alert information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    tracking_id: str

    alert_type: AlertType

    severity: AlertSeverity

    status: AlertStatus

    generated_at: datetime