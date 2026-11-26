"""
CRUD operations for the User model.
"""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.password import hash_password


class CRUDUser:
    """
    CRUD operations for the User model.
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

        db_user = User(
            full_name=user_in.full_name,
            email=user_in.email,
            password_hash=hash_password(user_in.password),
            role=user_in.role,
            is_active=user_in.is_active,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_user_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> User | None:
        """
        Retrieve a user by ID.
        """

        statement = select(User).where(User.id == user_id)

        return db.scalar(statement)

    def get_user_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """

        statement = select(User).where(User.email == email)

        return db.scalar(statement)
    
    def get_all_users(
        self,
        db: Session,
    ) -> list[User]:
        """
        Retrieve all users.
        """

        statement = select(User).order_by(User.id)

        return list(db.scalars(statement).all())

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_user(
        self,
        db: Session,
        db_user: User,
        user_in: UserUpdate,
    ) -> User:
        """
        Update user information.
        """

        update_data = user_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)

        return db_user

    # --------------------------------------------------------------------------
    # Activate / Deactivate
    # --------------------------------------------------------------------------

    def activate_user(
        self,
        db: Session,
        db_user: User,
    ) -> User:
        """
        Activate a user account.
        """

        db_user.is_active = True

        db.commit()
        db.refresh(db_user)

        return db_user

    def deactivate_user(
        self,
        db: Session,
        db_user: User,
    ) -> User:
        """
        Deactivate a user account.
        """

        db_user.is_active = False

        db.commit()
        db.refresh(db_user)

        return db_user

    # --------------------------------------------------------------------------
    # Last Login
    # --------------------------------------------------------------------------

    def update_last_login(
        self,
        db: Session,
        db_user: User,
    ) -> User:
        """
        Update the user's last login timestamp.
        """


        db_user.last_login_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_user)

        return db_user
    
# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

user_crud = CRUDUser()