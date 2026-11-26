"""
Bootstrap script for creating the initial administrator account.
Run only once during initial project setup.
"""

from sqlalchemy import select

from app.core.database import SessionLocal, engine
from app.db.base import Base
from app.enums.user import UserRole
from app.models.user import User
from app.utils.password import hash_password


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing_admin = db.scalar(
            select(User).where(
                User.role == UserRole.ADMINISTRATOR
            )
        )

        if existing_admin:
            print("Administrator already exists.")
            return

        admin = User(
            full_name="System Administrator",
            email="admin@example.com",
            password_hash=hash_password("Admin@123"),
            role=UserRole.ADMINISTRATOR,
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print("Administrator account created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()