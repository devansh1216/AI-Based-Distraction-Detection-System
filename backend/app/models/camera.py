"""
SQLAlchemy ORM model for the Cameras table.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Camera(Base):
    __tablename__ = "cameras"

    __table_args__ = (
        Index("ix_cameras_classroom_id", "classroom_id"),
        Index("ix_cameras_is_active", "is_active"),
        Index("ix_cameras_camera_type", "camera_type"),
        Index("ix_cameras_camera_name", "camera_name"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
    )

    classroom_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "classrooms.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    camera_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    camera_source: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    camera_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    resolution: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    fps: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
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

    # Relationships
    classroom = relationship(
        "Classroom",
        back_populates="cameras",
    )

    monitoring_sessions = relationship(
        "MonitoringSession",
        back_populates="camera",
        cascade="save-update, merge",
    )