"""
CRUD operations for the DetectionEvent model.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.detection_event import DetectionEvent
from app.schemas.detection_event import DetectionEventCreate
from app.enums.detection import BehaviourType

class CRUDDetectionEvent:
    """
    CRUD operations for the DetectionEvent model.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_detection_event(
        self,
        db: Session,
        event_in: DetectionEventCreate,
    ) -> DetectionEvent:
        """
        Create a new detection event.
        """

        db_event = DetectionEvent(
            session_id=event_in.session_id,
            tracking_id=event_in.tracking_id,
            representative_thumbnail=event_in.representative_thumbnail,
            behaviour_type=event_in.behaviour_type,
            confidence_score=event_in.confidence_score,
            event_timestamp=event_in.event_timestamp,
        )

        db.add(db_event)
        db.commit()
        db.refresh(db_event)

        return db_event

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_event_by_id(
        self,
        db: Session,
        event_id: int,
    ) -> DetectionEvent | None:
        """
        Retrieve a detection event by ID.
        """

        statement = select(DetectionEvent).where(
            DetectionEvent.id == event_id
        )

        return db.scalar(statement)

    def get_events_by_session(
        self,
        db: Session,
        session_id: int,
    ) -> list[DetectionEvent]:
        """
        Retrieve all detection events for a monitoring session.
        """

        statement = (
            select(DetectionEvent)
            .where(DetectionEvent.session_id == session_id)
            .order_by(DetectionEvent.event_timestamp)
        )

        return list(db.scalars(statement).all())
    
    def get_events_by_tracking_id(
        self,
        db: Session,
        tracking_id: str,
    ) -> list[DetectionEvent]:
        """
        Retrieve all detection events for a tracking ID.
        """

        statement = (
            select(DetectionEvent)
            .where(DetectionEvent.tracking_id == tracking_id)
            .order_by(DetectionEvent.event_timestamp)
        )

        return list(db.scalars(statement).all())
    
    def get_events_by_behaviour(
        self,
        db: Session,
        behaviour_type: BehaviourType,
    ) -> list[DetectionEvent]:
        """
        Retrieve all events of a specific behaviour type.
        """

        statement = (
            select(DetectionEvent)
            .where(
                DetectionEvent.behaviour_type == behaviour_type
            )
            .order_by(
                DetectionEvent.event_timestamp.desc()
            )
        )

        return list(db.scalars(statement).all())

    def get_all_events(
        self,
        db: Session,
    ) -> list[DetectionEvent]:
        """
        Retrieve all detection events.
        """

        statement = (
            select(DetectionEvent)
            .order_by(DetectionEvent.event_timestamp.desc())
        )

        return list(db.scalars(statement).all())


# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

detection_event_crud = CRUDDetectionEvent()