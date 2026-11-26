"""
SQLAlchemy ORM model for the Monitoring Sessions table.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Integer,
    Enum,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from app.enums.monitoring import (
    ReportStatus,
    SessionStatus,
)



class MonitoringSession(Base):
    __tablename__ = "monitoring_sessions"

    __table_args__ = (
        Index("ix_monitoring_sessions_user_id", "user_id"),
        Index("ix_monitoring_sessions_classroom_id", "classroom_id"),
        Index("ix_monitoring_sessions_camera_id", "camera_id"),
        Index("ix_monitoring_sessions_session_status", "session_status"),
        Index("ix_monitoring_sessions_started_at", "started_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    classroom_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "classrooms.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    camera_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "cameras.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    session_status: Mapped[str] = mapped_column(
        Enum(
            SessionStatus,
            name="session_status",
        ),
        nullable=False,
        server_default=text("'ACTIVE'"),
    )

    report_status: Mapped[str] = mapped_column(
        Enum(
            ReportStatus,
            name="report_status",
        ),
        nullable=False,
        server_default=text("'PENDING'"),
    )

    total_events: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )

    total_alerts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
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

    # Relationships

    user = relationship(
        "User",
        back_populates="monitoring_sessions",
    )

    classroom = relationship(
        "Classroom",
        back_populates="monitoring_sessions",
    )

    camera = relationship(
        "Camera",
        back_populates="monitoring_sessions",
    )

    detection_events = relationship(
        "DetectionEvent",
        back_populates="monitoring_session",
        cascade="save-update, merge",
    )

    alerts = relationship(
        "Alert",
        back_populates="monitoring_session",
        cascade="save-update, merge",
    )

    report = relationship(
        "Report",
        back_populates="monitoring_session",
        uselist=False,
        cascade="save-update, merge",
    )