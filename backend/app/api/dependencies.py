"""
Reusable authentication and authorization dependencies.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_access_token
from app.crud.crud_user import user_crud
from app.models.user import User
from app.schemas.auth import TokenPayload
from app.enums.user import UserRole


# ------------------------------------------------------------------------------
# OAuth2 Scheme
# ------------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


# ------------------------------------------------------------------------------
# Current User
# ------------------------------------------------------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Retrieve the currently authenticated user.
    """

    try:
        payload = TokenPayload(
            **verify_access_token(token)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        )

    user = user_crud.get_user_by_id(
        db=db,
        user_id=int(payload.sub),
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user

# ------------------------------------------------------------------------------
# Active User
# ------------------------------------------------------------------------------

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure the authenticated user account is active.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account.",
        )

    return current_user


# ------------------------------------------------------------------------------
# Role-Based Access Control (RBAC)
# ------------------------------------------------------------------------------

def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow access only to administrators.
    """

    if current_user.role != UserRole.ADMINISTRATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )

    return current_user


def require_teacher(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow access only to teachers.
    """

    if current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher privileges required.",
        )

    return current_user