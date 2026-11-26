"""
Business logic for detection event management.
"""

from sqlalchemy.orm import Session

from app.crud.crud_detection_event import detection_event_crud
from app.crud.crud_monitoring_session import monitoring_session_crud
from app.models.detection_event import DetectionEvent
from app.schemas.detection_event import DetectionEventCreate
from app.enums.monitoring import SessionStatus


class DetectionEventService:
    """
    Business logic for detection event management.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_detection_event(
        self,
        db: Session,
        event_in: DetectionEventCreate,
    ) -> DetectionEvent:
        
        session = monitoring_session_crud.get_session_by_id(
            db=db,
            session_id=event_in.session_id,
        )

        if session is None:
            raise ValueError("Monitoring session not found.")

        if session.session_status.name != SessionStatus.ACTIVE:
            raise ValueError(
                "Detection events can only be added to an active monitoring session."
            )

        event = detection_event_crud.create_detection_event(
            db=db,
            event_in=event_in,
        )

        monitoring_session_crud.increment_event_count(
            db=db,
            db_session=session,
        )

        return event

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_event(
        self,
        db: Session,
        event_id: int,
    ) -> DetectionEvent | None:
        
        return detection_event_crud.get_event_by_id(
            db=db,
            event_id=event_id,
        )

    def get_all_events(
        self,
        db: Session,
    ) -> list[DetectionEvent]:
        
        return detection_event_crud.get_all_events(
            db=db,
        )


# ------------------------------------------------------------------------------
# Singleton Service Instance
# ------------------------------------------------------------------------------

detection_event_service = DetectionEventService()