"""
CRUD operations for the AuditLog model.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate


class CRUDAuditLog:
    """
    CRUD operations for the AuditLog model.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_audit_log(
        self,
        db: Session,
        audit_log_in: AuditLogCreate,
    ) -> AuditLog:
        """
        Create a new audit log entry.
        """

        db_audit_log = AuditLog(
            user_id=audit_log_in.user_id,
            action_type=audit_log_in.action_type,
            action_description=audit_log_in.action_description,
            ip_address=audit_log_in.ip_address,
        )

        db.add(db_audit_log)
        db.commit()
        db.refresh(db_audit_log)

        return db_audit_log

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_audit_log_by_id(
        self,
        db: Session,
        audit_log_id: int,
    ) -> AuditLog | None:
        """
        Retrieve an audit log by ID.
        """

        statement = select(AuditLog).where(
            AuditLog.id == audit_log_id
        )

        return db.scalar(statement)

    def get_logs_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[AuditLog]:
        """
        Retrieve all audit logs for a user.
        """

        statement = (
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
        )

        return list(db.scalars(statement).all())

    def get_all_audit_logs(
        self,
        db: Session,
    ) -> list[AuditLog]:
        """
        Retrieve all audit logs.
        """

        statement = (
            select(AuditLog)
            .order_by(AuditLog.created_at.desc())
        )

        return list(db.scalars(statement).all())


# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

audit_log_crud = CRUDAuditLog()