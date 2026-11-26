"""
Monitoring session related enumerations.
"""

from enum import Enum


class SessionStatus(str, Enum):
    """
    Supported monitoring session statuses.
    """

    ACTIVE = "ACTIVE"
    FINALIZING = "FINALIZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ReportStatus(str, Enum):
    """
    Supported report generation statuses.
    """

    PENDING = "PENDING"
    GENERATING = "GENERATING"
    READY = "READY"
    FAILED = "FAILED"