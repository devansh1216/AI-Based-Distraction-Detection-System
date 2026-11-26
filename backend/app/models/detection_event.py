"""
SQLAlchemy ORM model for the Detection Events table.
"""

from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    Enum,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from app.enums.detection import BehaviourType


class DetectionEvent(Base):
    __tablename__ = "detection_events"

    __table_args__ = (
        Index("ix_detection_events_session_id", "session_id"),
        Index("ix_detection_events_tracking_id", "tracking_id"),
        Index("ix_detection_events_behaviour_type", "behaviour_type"),
        Index("ix_detection_events_event_timestamp", "event_timestamp"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
    )

    session_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "monitoring_sessions.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    tracking_id: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    representative_thumbnail: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    behaviour_type: Mapped[str] = mapped_column(
        Enum(
            BehaviourType,
            name="behaviour_type",
        ),
        nullable=False,
    )

    confidence_score: Mapped[Decimal] = mapped_column(
        Numeric(4, 3),
        nullable=False,
    )

    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships

    monitoring_session = relationship(
        "MonitoringSession",
        back_populates="detection_events",
    )