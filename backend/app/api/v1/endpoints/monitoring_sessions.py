"""
Monitoring Session API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.monitoring_session import (
    MonitoringSessionCreate,
    MonitoringSessionResponse,
    MonitoringSessionUpdate,
)
from app.services.monitoring_session_service import (
    monitoring_session_service,
)

router = APIRouter(
    prefix="/monitoring-sessions",
    tags=["Monitoring Sessions"],
)

# ------------------------------------------------------------------------------
# Create Monitoring Session
# ------------------------------------------------------------------------------

@router.post(
    "",
    response_model=MonitoringSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a monitoring session",
)
def create_session(
    session_in: MonitoringSessionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Create a new monitoring session.
    """

    try:
        return monitoring_session_service.create_session(
            db=db,
            session_in=session_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
        
# ------------------------------------------------------------------------------
# Get Monitoring Session
# ------------------------------------------------------------------------------

@router.get(
    "/{session_id}",
    response_model=MonitoringSessionResponse,
    summary="Get monitoring session by ID",
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve a monitoring session by ID.
    """

    session = monitoring_session_service.get_session(
        db=db,
        session_id=session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring session not found.",
        )

    return session

# ------------------------------------------------------------------------------
# Get All Monitoring Sessions
# ------------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[MonitoringSessionResponse],
    summary="Get all monitoring sessions",
)
def get_all_sessions(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve all monitoring sessions.
    """

    return monitoring_session_service.get_all_sessions(
        db=db,
    )
    
# ------------------------------------------------------------------------------
# Update Monitoring Session
# ------------------------------------------------------------------------------

@router.put(
    "/{session_id}",
    response_model=MonitoringSessionResponse,
    summary="Update monitoring session",
)
def update_session(
    session_id: int,
    session_in: MonitoringSessionUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Update monitoring session information.
    """

    session = monitoring_session_service.update_session(
        db=db,
        session_id=session_id,
        session_in=session_in,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring session not found.",
        )

    return session

# ------------------------------------------------------------------------------
# Complete Monitoring Session
# ------------------------------------------------------------------------------

@router.patch(
    "/{session_id}/complete",
    response_model=MonitoringSessionResponse,
    summary="Complete monitoring session",
)
def complete_session(
    session_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Complete a monitoring session.
    """

    session = monitoring_session_service.complete_session(
        db=db,
        session_id=session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitoring session not found.",
        )

    return session