"""
Detection Event API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.detection_event import (
    DetectionEventCreate,
    DetectionEventResponse,
)
from app.services.detection_event_service import (
    detection_event_service,
)

router = APIRouter(
    prefix="/detection-events",
    tags=["Detection Events"],
)

# ------------------------------------------------------------------------------
# Create Detection Event
# ------------------------------------------------------------------------------

@router.post(
    "",
    response_model=DetectionEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a detection event",
)
def create_detection_event(
    event_in: DetectionEventCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Create a new detection event.
    """

    try:
        return detection_event_service.create_detection_event(
            db=db,
            event_in=event_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
        
# ------------------------------------------------------------------------------
# Get Detection Event
# ------------------------------------------------------------------------------

@router.get(
    "/{event_id}",
    response_model=DetectionEventResponse,
    summary="Get detection event by ID",
)
def get_detection_event(
    event_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve a detection event by ID.
    """

    event = detection_event_service.get_event(
        db=db,
        event_id=event_id,
    )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection event not found.",
        )

    return event

# ------------------------------------------------------------------------------
# Get All Detection Events
# ------------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[DetectionEventResponse],
    summary="Get all detection events",
)
def get_all_detection_events(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve all detection events.
    """

    return detection_event_service.get_all_events(
        db=db,
    )