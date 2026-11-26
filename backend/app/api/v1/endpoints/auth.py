"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.auth import (
    ChangePasswordRequest,
    Token,
)
from app.services.auth_service import auth_service

# ------------------------------------------------------------------------------
# Router
# ------------------------------------------------------------------------------

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ------------------------------------------------------------------------------
# Login
# ------------------------------------------------------------------------------

@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT access token.
    """

    token = auth_service.login(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return token


# ------------------------------------------------------------------------------
# Current User
# ------------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user",
)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    """
    Return the currently authenticated user's profile.
    """

    return current_user

# ------------------------------------------------------------------------------
# Change Password
# ------------------------------------------------------------------------------

@router.post(
    "/change-password",
    summary="Change the password of the authenticated user",
)
def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Change the password of the currently authenticated user.
    """

    success = auth_service.change_password(
        db=db,
        user=current_user,
        current_password=password_data.current_password,
        new_password=password_data.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    return {
        "message": "Password changed successfully.",
    }