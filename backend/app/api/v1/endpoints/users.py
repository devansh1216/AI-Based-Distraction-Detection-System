"""
User management API endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import user_service


# ------------------------------------------------------------------------------
# Router
# ------------------------------------------------------------------------------

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ------------------------------------------------------------------------------
# Create User
# ------------------------------------------------------------------------------

@router.post(
    "",
    response_model=UserResponse,
    summary="Create a new user",
)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Create a new user.
    """

    return user_service.create_user(
        db=db,
        user_in=user_in,
    )


# ------------------------------------------------------------------------------
# Get All Users
# ------------------------------------------------------------------------------

@router.get(
    "",
    response_model=UserListResponse,
    summary="Retrieve all users",
)
def get_all_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve all users.
    """

    users = user_service.get_all_users(
        db=db,
    )

    return UserListResponse(
        users=users,
        total=len(users),
    )
    
# ------------------------------------------------------------------------------
# Get User by ID
# ------------------------------------------------------------------------------

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Retrieve a user by ID",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve a user by ID.
    """

    return user_service.get_user(
        db=db,
        user_id=user_id,
    )


# ------------------------------------------------------------------------------
# Update User
# ------------------------------------------------------------------------------

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Update user information.
    """

    return user_service.update_user(
        db=db,
        user_id=user_id,
        user_in=user_in,
    )


# ------------------------------------------------------------------------------
# Activate User
# ------------------------------------------------------------------------------

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
    summary="Activate a user",
)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Activate a user account.
    """

    return user_service.activate_user(
        db=db,
        user_id=user_id,
    )


# ------------------------------------------------------------------------------
# Deactivate User
# ------------------------------------------------------------------------------

@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
    summary="Deactivate a user",
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Deactivate a user account.
    """

    return user_service.deactivate_user(
        db=db,
        user_id=user_id,
    )