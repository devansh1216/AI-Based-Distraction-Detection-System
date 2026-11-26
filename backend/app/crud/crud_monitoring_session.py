"""
CRUD operations for the MonitoringSession model.
"""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.monitoring import SessionStatus
from app.models.monitoring_session import MonitoringSession
from app.schemas.monitoring_session import (
    MonitoringSessionCreate,
    MonitoringSessionUpdate,
)


class CRUDMonitoringSession:
    """
    CRUD operations for the MonitoringSession model.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_session(
        self,
        db: Session,
        session_in: MonitoringSessionCreate,
    ) -> MonitoringSession:
        """
        Create a new monitoring session.
        """
        
        db_session = MonitoringSession(
            user_id=session_in.user_id,
            classroom_id=session_in.classroom_id,
            camera_id=session_in.camera_id,
            session_status=SessionStatus.ACTIVE,
            started_at=datetime.now(timezone.utc),
        )

        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        return db_session

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_session_by_id(
        self,
        db: Session,
        session_id: int,
    ) -> MonitoringSession | None:
        """
        Retrieve a monitoring session by ID.
        """

        statement = select(MonitoringSession).where(
            MonitoringSession.id == session_id
        )

        return db.scalar(statement)

    def get_active_session(
        self,
        db: Session,
        camera_id: int,
    ) -> MonitoringSession | None:
        """
        Retrieve the active monitoring session for a camera.
        """

        statement = select(MonitoringSession).where(
            MonitoringSession.camera_id == camera_id,
            MonitoringSession.session_status == SessionStatus.ACTIVE,
        )

        return db.scalar(statement)
    
    def get_sessions_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[MonitoringSession]:
        """
        Retrieve all monitoring sessions for a user.
        """

        statement = (
            select(MonitoringSession)
            .where(MonitoringSession.user_id == user_id)
            .order_by(MonitoringSession.started_at.desc())
        )

        return list(db.scalars(statement).all())

    def get_sessions_by_classroom(
        self,
        db: Session,
        classroom_id: int,
    ) -> list[MonitoringSession]:
        """
        Retrieve all monitoring sessions for a classroom.
        """

        statement = (
            select(MonitoringSession)
            .where(MonitoringSession.classroom_id == classroom_id)
            .order_by(MonitoringSession.started_at.desc())
        )

        return list(db.scalars(statement).all())

    def get_all_sessions(
        self,
        db: Session,
    ) -> list[MonitoringSession]:
        """
        Retrieve all monitoring sessions.
        """

        statement = (
            select(MonitoringSession)
            .order_by(MonitoringSession.started_at.desc())
        )

        return list(db.scalars(statement).all())

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_session(
        self,
        db: Session,
        db_session: MonitoringSession,
        session_in: MonitoringSessionUpdate,
    ) -> MonitoringSession:
        """
        Update monitoring session information.
        """

        update_data = session_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_session, field, value)

        db.commit()
        db.refresh(db_session)

        return db_session
    
    # --------------------------------------------------------------------------
    # Session Lifecycle
    # --------------------------------------------------------------------------

    def complete_session(
        self,
        db: Session,
        db_session: MonitoringSession,
    ) -> MonitoringSession:
        """
        Mark a monitoring session as completed.
        """

        db_session.session_status = SessionStatus.COMPLETED
        db_session.ended_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_session)

        return db_session

    # --------------------------------------------------------------------------
    # Counters
    # --------------------------------------------------------------------------

    def increment_event_count(
        self,
        db: Session,
        db_session: MonitoringSession,
    ) -> MonitoringSession:
        """
        Increment the total detected events count.
        """

        db_session.total_events += 1

        db.commit()
        db.refresh(db_session)

        return db_session

    def increment_alert_count(
        self,
        db: Session,
        db_session: MonitoringSession,
    ) -> MonitoringSession:
        """
        Increment the total generated alerts count.
        """

        db_session.total_alerts += 1

        db.commit()
        db.refresh(db_session)

        return db_session


# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

monitoring_session_crud = CRUDMonitoringSession()