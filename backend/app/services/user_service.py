"""
Business logic for user management.
"""

from app.crud.crud_user import user_crud
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    DuplicateResourceException,
    UserNotFoundException,
)


class UserService:
    """
    Business logic for user management.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_user(
        self,
        db: Session,
        user_in: UserCreate,
    ) -> User:
        """
        Create a new user.
        """

        existing_user = user_crud.get_user_by_email(
            db=db,
            email=user_in.email,
        )

        if existing_user is not None:
            raise DuplicateResourceException(
                "A user with this email already exists."
            )

        return user_crud.create_user(
            db=db,
            user_in=user_in,
        )

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_user(
        self,
        db: Session,
        user_id: int,
    ) -> User:
        """
        Retrieve a user by ID.
        """

        user = user_crud.get_user_by_id(
            db=db,
            user_id=user_id,
        )

        if user is None:
            raise UserNotFoundException(
                "User not found."
            )

        return user

    def get_all_users(
        self,
        db: Session,
    ) -> list[User]:
        """
        Retrieve all users.
        """

        return user_crud.get_all_users(
            db=db,
        )
        
    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_user(
        self,
        db: Session,
        user_id: int,
        user_in: UserUpdate,
    ) -> User:
        """
        Update user information.
        """

        db_user = self.get_user(
            db=db,
            user_id=user_id,
        )

        if (
            user_in.email is not None
            and user_in.email != db_user.email
        ):
            existing_user = user_crud.get_user_by_email(
                db=db,
                email=user_in.email,
            )

            if existing_user is not None:
                raise DuplicateResourceException(
                    "A user with this email already exists."
                )

        return user_crud.update_user(
            db=db,
            db_user=db_user,
            user_in=user_in,
        )

    # --------------------------------------------------------------------------
    # Activate / Deactivate
    # --------------------------------------------------------------------------

    def activate_user(
        self,
        db: Session,
        user_id: int,
    ) -> User:
        """
        Activate a user account.
        """

        db_user = self.get_user(
            db=db,
            user_id=user_id,
        )

        return user_crud.activate_user(
            db=db,
            db_user=db_user,
        )

    def deactivate_user(
        self,
        db: Session,
        user_id: int,
    ) -> User:
        """
        Deactivate a user account.
        """

        db_user = self.get_user(
            db=db,
            user_id=user_id,
        )

        return user_crud.deactivate_user(
            db=db,
            db_user=db_user,
        )


# ------------------------------------------------------------------------------
# Singleton Service Instance
# ------------------------------------------------------------------------------

user_service = UserService()