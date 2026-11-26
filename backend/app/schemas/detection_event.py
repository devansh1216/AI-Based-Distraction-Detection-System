"""
Detection Event related Pydantic schemas.
"""

from datetime import datetime
from decimal import Decimal
from app.enums.detection import BehaviourType

from pydantic import ConfigDict, Field

from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Base Schema
# ------------------------------------------------------------------------------


class DetectionEventBase(BaseSchema):
    """
    Base schema shared across detection event schemas.
    """

    session_id: int = Field(..., gt=0)

    tracking_id: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    representative_thumbnail: str | None = Field(
        default=None,
        max_length=255,
    )

    behaviour_type: BehaviourType

    confidence_score: Decimal = Field(
        ...,
        ge=Decimal("0.000"),
        le=Decimal("1.000"),
    )

    event_timestamp: datetime


# ------------------------------------------------------------------------------
# Create Schema
# ------------------------------------------------------------------------------


class DetectionEventCreate(DetectionEventBase):
    """
    Schema received from the AI Detection Engine.
    """

    pass


# ------------------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------------------


class DetectionEventUpdate(BaseSchema):
    """
    Detection events are immutable after creation.

    This schema is intentionally left empty to preserve
    historical integrity.
    """

    pass


# ------------------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------------------


class DetectionEventResponse(DetectionEventBase):
    """
    Detection event returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    created_at: datetime


# ------------------------------------------------------------------------------
# Summary Schema
# ------------------------------------------------------------------------------


class DetectionEventSummary(BaseSchema):
    """
    Lightweight detection event representation.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    tracking_id: str

    behaviour_type: BehaviourType

    confidence_score: Decimal

    event_timestamp: datetime