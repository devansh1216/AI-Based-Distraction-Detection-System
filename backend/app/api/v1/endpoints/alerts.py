"""
Alert management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.alert import (
    AlertCreate,
    AlertResponse,
    AlertUpdate,
)
from app.services.alert_service import alert_service

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)

# ------------------------------------------------------------------------------
# Create Alert
# ------------------------------------------------------------------------------

@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new alert",
)
def create_alert(
    alert_in: AlertCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Create a new alert.
    """

    try:
        return alert_service.create_alert(
            db=db,
            alert_in=alert_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
        
# ------------------------------------------------------------------------------
# Get Alert
# ------------------------------------------------------------------------------

@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
    summary="Get alert by ID",
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve an alert by ID.
    """

    alert = alert_service.get_alert(
        db=db,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return alert

# --------------------------------------------------------------------------
# Get All Alerts
# --------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[AlertResponse],
    summary="Get all alerts",
)
def get_all_alerts(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve all alerts.
    """

    return alert_service.get_all_alerts(
        db=db,
    )

# ------------------------------------------------------------------------------
# Update Alert
# ------------------------------------------------------------------------------

@router.put(
    "/{alert_id}",
    response_model=AlertResponse,
    summary="Update alert",
)
def update_alert(
    alert_id: int,
    alert_in: AlertUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Update alert information.
    """

    alert = alert_service.update_alert(
        db=db,
        alert_id=alert_id,
        alert_in=alert_in,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return alert

# ------------------------------------------------------------------------------
# Acknowledge Alert
# ------------------------------------------------------------------------------

@router.patch(
    "/{alert_id}/acknowledge",
    response_model=AlertResponse,
    summary="Acknowledge alert",
)
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Mark an alert as acknowledged.
    """

    alert = alert_service.acknowledge_alert(
        db=db,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return alert

# ------------------------------------------------------------------------------
# Dismiss Alert
# ------------------------------------------------------------------------------

@router.patch(
    "/{alert_id}/dismiss",
    response_model=AlertResponse,
    summary="Dismiss alert",
)
def dismiss_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Mark an alert as dismissed.
    """

    alert = alert_service.dismiss_alert(
        db=db,
        alert_id=alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )

    return alert