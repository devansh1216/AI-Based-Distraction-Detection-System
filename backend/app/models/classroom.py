"""
SQLAlchemy ORM model for the Classrooms table.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Index,
    Integer,
    SmallInteger,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    __table_args__ = (
        Index("ix_classrooms_classroom_code", "classroom_code"),
        Index("ix_classrooms_building_name", "building_name"),
        Index("ix_classrooms_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
    )

    classroom_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    classroom_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    floor_number: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
    )

    building_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    max_capacity: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
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

    cameras = relationship(
        "Camera",
        back_populates="classroom",
        cascade="save-update, merge",
    )

    monitoring_sessions = relationship(
        "MonitoringSession",
        back_populates="classroom",
        cascade="save-update, merge",
    )