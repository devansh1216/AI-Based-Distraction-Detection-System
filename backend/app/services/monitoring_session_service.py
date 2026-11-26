"""
Business logic for monitoring session management.
"""

from sqlalchemy.orm import Session

from app.crud.crud_camera import camera_crud
from app.crud.crud_classroom import classroom_crud
from app.crud.crud_monitoring_session import monitoring_session_crud
from app.crud.crud_user import user_crud
from app.models.monitoring_session import MonitoringSession
from app.schemas.monitoring_session import (
    MonitoringSessionCreate,
    MonitoringSessionUpdate,
)


class MonitoringSessionService:
    """
    Business logic for monitoring session management.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_session(
        self,
        db: Session,
        session_in: MonitoringSessionCreate,
    ) -> MonitoringSession:
        
        user = user_crud.get_user_by_id(
            db=db,
            user_id=session_in.user_id,
        )

        if user is None:
            raise ValueError("User not found.")

        classroom = classroom_crud.get_classroom_by_id(
            db=db,
            classroom_id=session_in.classroom_id,
        )

        if classroom is None:
            raise ValueError("Classroom not found.")

        camera = camera_crud.get_camera_by_id(
            db=db,
            camera_id=session_in.camera_id,
        )

        if camera is None:
            raise ValueError("Camera not found.")

        if camera.classroom_id != classroom.id:
            raise ValueError(
                "Camera does not belong to the specified classroom."
            )

        active_session = monitoring_session_crud.get_active_session(
            db=db,
            camera_id=session_in.camera_id,
        )

        if active_session is not None:
            raise ValueError(
                "An active monitoring session already exists for this camera."
            )

        return monitoring_session_crud.create_session(
            db=db,
            session_in=session_in,
        )

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_session(
        self,
        db: Session,
        session_id: int,
    ) -> MonitoringSession | None:
        
        return monitoring_session_crud.get_session_by_id(
            db=db,
            session_id=session_id,
        )

    def get_all_sessions(
        self,
        db: Session,
    ) -> list[MonitoringSession]:
        
        return monitoring_session_crud.get_all_sessions(
            db=db,
        )

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_session(
        self,
        db: Session,
        session_id: int,
        session_in: MonitoringSessionUpdate,
    ) -> MonitoringSession | None:
        
        db_session = monitoring_session_crud.get_session_by_id(
            db=db,
            session_id=session_id,
        )

        if db_session is None:
            return None

        return monitoring_session_crud.update_session(
            db=db,
            db_session=db_session,
            session_in=session_in,
        )

    # --------------------------------------------------------------------------
    # Session Lifecycle
    # --------------------------------------------------------------------------

    def complete_session(
        self,
        db: Session,
        session_id: int,
    ) -> MonitoringSession | None:
        
        db_session = monitoring_session_crud.get_session_by_id(
            db=db,
            session_id=session_id,
        )
        
        if db_session is None:
            return None
        
        return monitoring_session_crud.complete_session(
            db=db,
            db_session=db_session,
        )


# ------------------------------------------------------------------------------
# Singleton Service Instance
# ------------------------------------------------------------------------------

monitoring_session_service = MonitoringSessionService()