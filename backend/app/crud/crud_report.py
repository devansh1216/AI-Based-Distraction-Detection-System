"""
CRUD operations for the Report model.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate
from datetime import datetime, timezone

from app.enums.report import ReportStatus


class CRUDReport:
    """
    CRUD operations for the Report model.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_report(
        self,
        db: Session,
        report_in: ReportCreate,
    ) -> Report:
        """
        Create a new report.
        """

        db_report = Report(
            session_id=report_in.session_id,
            report_name=report_in.report_name,
            report_path=report_in.report_path,
            report_status=report_in.report_status,
            generated_at=report_in.generated_at,
        )

        db.add(db_report)
        db.commit()
        db.refresh(db_report)

        return db_report

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_report_by_id(
        self,
        db: Session,
        report_id: int,
    ) -> Report | None:
        """
        Retrieve a report by ID.
        """

        statement = select(Report).where(
            Report.id == report_id
        )

        return db.scalar(statement)

    def get_report_by_session(
        self,
        db: Session,
        session_id: int,
    ) -> Report | None:
        """
        Retrieve the report for a monitoring session.
        """

        statement = select(Report).where(
            Report.session_id == session_id
        )

        return db.scalar(statement)

    def get_all_reports(
        self,
        db: Session,
    ) -> list[Report]:
        """
        Retrieve all reports.
        """

        statement = (
            select(Report)
            .order_by(Report.created_at.desc())
        )

        return list(db.scalars(statement).all())

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_report(
        self,
        db: Session,
        db_report: Report,
        report_in: ReportUpdate,
    ) -> Report:
        """
        Update report information.
        """

        update_data = report_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_report, field, value)

        db.commit()
        db.refresh(db_report)

        return db_report
    
    # --------------------------------------------------------------------------
    # Report Actions
    # --------------------------------------------------------------------------

    def mark_report_generated(
        self,
        db: Session,
        db_report: Report,
    ) -> Report:
        """
        Mark a report as generated.
        """

        db_report.report_status = ReportStatus.READY
        db_report.generated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_report)

        return db_report


# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

report_crud = CRUDReport()