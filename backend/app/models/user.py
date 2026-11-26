"""
SQLAlchemy ORM model for the Users table.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    BigInteger,
    Boolean,
    DateTime,
    Index,
    Integer,
    String,
    text,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from app.enums.user import UserRole


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_role", "role"),
        Index("ix_users_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
        ),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    monitoring_sessions = relationship(
        "MonitoringSession",
        back_populates="user",
        cascade="save-update, merge",
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        cascade="save-update, merge",
    )