"""
SQLAlchemy ORM model for the Alerts table.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Enum,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

from app.enums.alert import (
    AlertSeverity,
    AlertStatus,
    AlertType,
)


class Alert(Base):
    __tablename__ = "alerts"

    __table_args__ = (
        Index("ix_alerts_session_id", "session_id"),
        Index("ix_alerts_tracking_id", "tracking_id"),
        Index("ix_alerts_alert_type", "alert_type"),
        Index("ix_alerts_generated_at", "generated_at"),
        Index("ix_alerts_status", "status"),
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

    alert_type: Mapped[str] = mapped_column(
        Enum(
            AlertType,
            name="alert_type",
        ),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        Enum(
            AlertSeverity,
            name="alert_severity",
        ),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        Enum(
            AlertStatus,
            name="alert_status",
        ),
        nullable=False,
        server_default=text("'ACTIVE'"),
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships

    monitoring_session = relationship(
        "MonitoringSession",
        back_populates="alerts",
    )