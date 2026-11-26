"""
Report management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.report import (
    ReportCreate,
    ReportResponse,
    ReportUpdate,
)
from app.services.report_service import report_service

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

# ------------------------------------------------------------------------------
# Create Report
# ------------------------------------------------------------------------------

@router.post(
    "",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new report",
)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Create a new report.
    """

    try:
        return report_service.create_report(
            db=db,
            report_in=report_in,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ------------------------------------------------------------------------------
# Get Report
# ------------------------------------------------------------------------------

@router.get(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Get report by ID",
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve a report by ID.
    """

    report = report_service.get_report(
        db=db,
        report_id=report_id,
    )

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    return report


# ------------------------------------------------------------------------------
# Get All Reports
# ------------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[ReportResponse],
    summary="Get all reports",
)
def get_all_reports(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Retrieve all reports.
    """

    return report_service.get_all_reports(
        db=db,
    )


# ------------------------------------------------------------------------------
# Update Report
# ------------------------------------------------------------------------------

@router.put(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Update report",
)
def update_report(
    report_id: int,
    report_in: ReportUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Update report information.
    """

    report = report_service.update_report(
        db=db,
        report_id=report_id,
        report_in=report_in,
    )

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    return report


# ------------------------------------------------------------------------------
# Generate Report
# ------------------------------------------------------------------------------

@router.patch(
    "/{report_id}/generate",
    response_model=ReportResponse,
    summary="Mark report as generated",
)
def generate_report(
    report_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Mark a report as generated.
    """

    try:
        report = report_service.mark_report_generated(
            db=db,
            report_id=report_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    return report