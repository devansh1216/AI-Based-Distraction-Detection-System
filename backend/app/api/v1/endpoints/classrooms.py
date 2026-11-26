"""
Classroom management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.classroom import (
    ClassroomCreate,
    ClassroomResponse,
    ClassroomUpdate,
)
from app.services.classroom_service import classroom_service

router = APIRouter(
    prefix="/classrooms",
    tags=["Classrooms"],
)

# ------------------------------------------------------------------------------
# Create Classroom
# ------------------------------------------------------------------------------

@router.post(
    "",
    response_model=ClassroomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new classroom",
)
def create_classroom(
    classroom_in: ClassroomCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Create a new classroom.
    """

    try:
        return classroom_service.create_classroom(
            db=db,
            classroom_in=classroom_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
        
# ------------------------------------------------------------------------------
# Get Classroom
# ------------------------------------------------------------------------------

@router.get(
    "/{classroom_id}",
    response_model=ClassroomResponse,
    summary="Get classroom by ID",
)
def get_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve a classroom by ID.
    """

    classroom = classroom_service.get_classroom(
        db=db,
        classroom_id=classroom_id,
    )

    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found.",
        )

    return classroom

# ------------------------------------------------------------------------------
# Get All Classrooms
# ------------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[ClassroomResponse],
    summary="Get all classrooms",
)
def get_all_classrooms(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve all classrooms.
    """

    return classroom_service.get_all_classrooms(
        db=db,
    )
    
# ------------------------------------------------------------------------------
# Update Classroom
# ------------------------------------------------------------------------------

@router.put(
    "/{classroom_id}",
    response_model=ClassroomResponse,
    summary="Update classroom",
)
def update_classroom(
    classroom_id: int,
    classroom_in: ClassroomUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Update classroom information.
    """

    try:
        classroom = classroom_service.update_classroom(
            db=db,
            classroom_id=classroom_id,
            classroom_in=classroom_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found.",
        )

    return classroom

# ------------------------------------------------------------------------------
# Activate Classroom
# ------------------------------------------------------------------------------

@router.patch(
    "/{classroom_id}/activate",
    response_model=ClassroomResponse,
    summary="Activate classroom",
)
def activate_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Activate a classroom.
    """

    classroom = classroom_service.activate_classroom(
        db=db,
        classroom_id=classroom_id,
    )

    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found.",
        )

    return classroom

# ------------------------------------------------------------------------------
# Deactivate Classroom
# ------------------------------------------------------------------------------

@router.patch(
    "/{classroom_id}/deactivate",
    response_model=ClassroomResponse,
    summary="Deactivate classroom",
)
def deactivate_classroom(
    classroom_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Deactivate a classroom.
    """

    classroom = classroom_service.deactivate_classroom(
        db=db,
        classroom_id=classroom_id,
    )

    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found.",
        )

    return classroom