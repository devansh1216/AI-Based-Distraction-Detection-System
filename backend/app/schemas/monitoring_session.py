"""
Monitoring Session related Pydantic schemas.
"""

from datetime import datetime

from pydantic import ConfigDict, Field

from app.enums.monitoring import ReportStatus, SessionStatus
from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class MonitoringSessionCreate(BaseSchema):
    """
    Schema used when creating a monitoring session.
    """

    user_id: int = Field(..., gt=0)

    classroom_id: int = Field(..., gt=0)

    camera_id: int = Field(..., gt=0)


# ------------------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------------------


class MonitoringSessionUpdate(BaseSchema):
    """
    Schema used when updating a monitoring session.
    """

    session_status: SessionStatus | None = None

    report_status: ReportStatus | None = None

    total_events: int | None = Field(
        default=None,
        ge=0,
    )

    total_alerts: int | None = Field(
        default=None,
        ge=0,
    )

    ended_at: datetime | None = None


# ------------------------------------------------------------------------------
# Start Monitoring Request
# ------------------------------------------------------------------------------


class StartMonitoringRequest(BaseSchema):
    """
    Request body for starting a monitoring session.
    """

    classroom_id: int = Field(..., gt=0)

    camera_id: int = Field(..., gt=0)


# ------------------------------------------------------------------------------
# Stop Monitoring Request
# ------------------------------------------------------------------------------


class StopMonitoringRequest(BaseSchema):
    """
    Request body for stopping a monitoring session.
    """

    session_id: int = Field(..., gt=0)


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class MonitoringSessionResponse(BaseSchema):
    """
    Monitoring session returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    user_id: int

    classroom_id: int

    camera_id: int

    session_status: SessionStatus

    report_status: ReportStatus

    total_events: int

    total_alerts: int

    started_at: datetime

    ended_at: datetime | None

    created_at: datetime

    updated_at: datetime


# ------------------------------------------------------------------------------
# Summary Schema
# ------------------------------------------------------------------------------


class MonitoringSessionSummary(BaseSchema):
    """
    Lightweight monitoring session information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    classroom_id: int

    camera_id: int

    session_status: SessionStatus

    started_at: datetime

    ended_at: datetime | None