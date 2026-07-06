"""
Imports all ORM models so SQLAlchemy and Alembic
can discover them through Base.metadata.
"""

from app.db.base_class import Base

from app.models.user import User
from app.models.classroom import Classroom
from app.models.camera import Camera
from app.models.monitoring_session import MonitoringSession
from app.models.detection_event import DetectionEvent
from app.models.alert import Alert
from app.models.report import Report
from app.models.audit_log import AuditLog