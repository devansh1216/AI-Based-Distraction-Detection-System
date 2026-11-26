"""
SQLAlchemy ORM model for the Reports table.
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

from app.enums.report import ReportStatus


class Report(Base):
    __tablename__ = "reports"

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
        unique=True,
    )

    report_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    report_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    report_status: Mapped[str] = mapped_column(
        Enum(
            ReportStatus,
            name="report_status",
        ),
        nullable=False,
        server_default=text("'PENDING'"),
    )

    generated_at: Mapped[datetime | None] = mapped_column(
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
        back_populates="report",
    )

    # Indexes

    __table_args__ = (
        Index("ix_reports_session_id", "session_id"),
        Index("ix_reports_report_status", "report_status"),
        Index("ix_reports_generated_at", "generated_at"),
    )