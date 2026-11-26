"""
Authentication service.
"""

from app.utils.password import (
    hash_password,
    verify_password,
)

from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.crud.crud_user import user_crud
from app.models.user import User
from app.schemas.auth import Token


class AuthService:
    """
    Business logic for authentication.
    """

    # --------------------------------------------------------------------------
    # Authentication
    # --------------------------------------------------------------------------

    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> User | None:
        """
        Authenticate a user using email and password.
        """

        user = user_crud.get_user_by_email(
            db=db,
            email=email,
        )

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user

    # --------------------------------------------------------------------------
    # JWT
    # --------------------------------------------------------------------------

    def create_access_token_for_user(
        self,
        user: User,
    ) -> Token:
        """
        Create a JWT access token for an authenticated user.
        """

        access_token = create_access_token(
            subject=str(user.id),
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )
        
    # --------------------------------------------------------------------------
    # Login
    # --------------------------------------------------------------------------

    def login(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> Token | None:
        """
        Authenticate the user and return a JWT access token.
        """

        user = self.authenticate_user(
            db=db,
            email=email,
            password=password,
        )

        if user is None:
            return None

        user_crud.update_last_login(
            db=db,
            db_user=user,
        )

        return self.create_access_token_for_user(user)

    # --------------------------------------------------------------------------
    # Password Management
    # --------------------------------------------------------------------------

    def change_password(
        self,
        db: Session,
        user: User,
        current_password: str,
        new_password: str,
    ) -> bool:
        """
        Change the password of an authenticated user.
        """

        if not verify_password(
            current_password,
            user.password_hash,
        ):
            return False

        user.password_hash = hash_password(new_password)

        db.commit()
        db.refresh(user)

        return True


# ------------------------------------------------------------------------------
# Singleton Service Instance
# ------------------------------------------------------------------------------

auth_service = AuthService()