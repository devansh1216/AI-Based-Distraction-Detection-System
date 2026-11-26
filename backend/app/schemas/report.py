"""
Report-related Pydantic schemas.
"""

from datetime import datetime
from app.enums.report import ReportStatus

from pydantic import ConfigDict, Field

from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Base Schema
# ------------------------------------------------------------------------------


class ReportBase(BaseSchema):
    """
    Base schema shared across report schemas.
    """

    session_id: int = Field(
        ...,
        gt=0,
    )

    report_name: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )

    report_path: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    report_status: ReportStatus = ReportStatus.PENDING

    generated_at: datetime | None = None


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class ReportCreate(ReportBase):
    """
    Schema used internally when creating reports.
    """

    pass


# ------------------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------------------


class ReportUpdate(BaseSchema):
    """
    Schema used while updating report generation status.
    """

    report_status: ReportStatus | None = None

    generated_at: datetime | None = None

    report_path: str | None = Field(
        default=None,
        max_length=255,
    )


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class ReportResponse(ReportBase):
    """
    Report returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime


# ------------------------------------------------------------------------------
# Summary Schema
# ------------------------------------------------------------------------------


class ReportSummary(BaseSchema):
    """
    Lightweight report information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    session_id: int

    report_name: str

    report_status: ReportStatus

    generated_at: datetime | None