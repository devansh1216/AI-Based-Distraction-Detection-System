"""
Business logic for report management.
"""

from sqlalchemy.orm import Session

from app.crud.crud_monitoring_session import monitoring_session_crud
from app.crud.crud_report import report_crud
from app.enums.monitoring import SessionStatus
from app.models.report import Report
from app.schemas.report import (
    ReportCreate,
    ReportUpdate,
)


class ReportService:
    """
    Business logic for report management.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_report(
        self,
        db: Session,
        report_in: ReportCreate,
    ) -> Report:

        db_session = monitoring_session_crud.get_session_by_id(
            db=db,
            session_id=report_in.session_id,
        )

        if db_session is None:
            raise ValueError("Monitoring session not found.")

        if db_session.session_status != SessionStatus.COMPLETED:
            raise ValueError(
                "Reports can only be created for completed monitoring sessions."
            )

        existing_report = report_crud.get_report_by_session(
            db=db,
            session_id=report_in.session_id,
        )

        if existing_report is not None:
            raise ValueError(
                "A report already exists for this monitoring session."
            )

        return report_crud.create_report(
            db=db,
            report_in=report_in,
        )

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_report(
        self,
        db: Session,
        report_id: int,
    ) -> Report | None:

        return report_crud.get_report_by_id(
            db=db,
            report_id=report_id,
        )

    def get_all_reports(
        self,
        db: Session,
    ) -> list[Report]:

        return report_crud.get_all_reports(
            db=db,
        )

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_report(
        self,
        db: Session,
        report_id: int,
        report_in: ReportUpdate,
    ) -> Report | None:

        db_report = report_crud.get_report_by_id(
            db=db,
            report_id=report_id,
        )

        if db_report is None:
            return None

        return report_crud.update_report(
            db=db,
            db_report=db_report,
            report_in=report_in,
        )

    # --------------------------------------------------------------------------
    # Report Actions
    # --------------------------------------------------------------------------

    def mark_report_generated(
        self,
        db: Session,
        report_id: int,
    ) -> Report | None:

        db_report = report_crud.get_report_by_id(
            db=db,
            report_id=report_id,
        )

        if db_report is None:
            return None

        if db_report.report_status.name == "GENERATED":
            raise ValueError(
                "Report has already been generated."
            )

        return report_crud.mark_report_generated(
            db=db,
            db_report=db_report,
        )


report_service = ReportService()