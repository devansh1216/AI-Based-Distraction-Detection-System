"""
Camera management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.camera import (
    CameraCreate,
    CameraResponse,
    CameraUpdate,
)
from app.services.camera_service import camera_service

router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"],
)

# ------------------------------------------------------------------------------
# Create Camera
# ------------------------------------------------------------------------------

@router.post(
    "",
    response_model=CameraResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new camera",
)
def create_camera(
    camera_in: CameraCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Register a new camera.
    """

    try:
        return camera_service.create_camera(
            db=db,
            camera_in=camera_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
        
# ------------------------------------------------------------------------------
# Get Camera
# ------------------------------------------------------------------------------

@router.get(
    "/{camera_id}",
    response_model=CameraResponse,
    summary="Get camera by ID",
)
def get_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve a camera by ID.
    """

    camera = camera_service.get_camera(
        db=db,
        camera_id=camera_id,
    )

    if camera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found.",
        )

    return camera

# ------------------------------------------------------------------------------
# Get All Cameras
# ------------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[CameraResponse],
    summary="Get all cameras",
)
def get_all_cameras(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve all registered cameras.
    """

    return camera_service.get_all_cameras(
        db=db,
    )
    
# ------------------------------------------------------------------------------
# Update Camera
# ------------------------------------------------------------------------------

@router.put(
    "/{camera_id}",
    response_model=CameraResponse,
    summary="Update camera",
)
def update_camera(
    camera_id: int,
    camera_in: CameraUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Update camera information.
    """

    try:
        camera = camera_service.update_camera(
            db=db,
            camera_id=camera_id,
            camera_in=camera_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if camera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found.",
        )

    return camera

# ------------------------------------------------------------------------------
# Activate Camera
# ------------------------------------------------------------------------------

@router.patch(
    "/{camera_id}/activate",
    response_model=CameraResponse,
    summary="Activate camera",
)
def activate_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Activate a camera.
    """

    camera = camera_service.activate_camera(
        db=db,
        camera_id=camera_id,
    )

    if camera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found.",
        )

    return camera

# ------------------------------------------------------------------------------
# Deactivate Camera
# ------------------------------------------------------------------------------

@router.patch(
    "/{camera_id}/deactivate",
    response_model=CameraResponse,
    summary="Deactivate camera",
)
def deactivate_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Deactivate a camera.
    """

    camera = camera_service.deactivate_camera(
        db=db,
        camera_id=camera_id,
    )

    if camera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found.",
        )

    return camera