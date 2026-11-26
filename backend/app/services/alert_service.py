from app.crud.crud_alert import alert_crud
from app.crud.crud_monitoring_session import monitoring_session_crud
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate
from app.enums.monitoring import SessionStatus
from sqlalchemy.orm import Session

class AlertService:

    # Create

    def create_alert(
        self,
        db: Session,
        alert_in: AlertCreate,
    ) -> Alert:

        db_session = monitoring_session_crud.get_session_by_id(
            db=db,
            session_id=alert_in.session_id,
        )

        if db_session is None:
            raise ValueError("Monitoring session not found.")

        if db_session.session_status != SessionStatus.ACTIVE:
            raise ValueError(
                "Alerts can only be generated for an active monitoring session."
            )

        db_alert = alert_crud.create_alert(
            db=db,
            alert_in=alert_in,
        )

        monitoring_session_crud.increment_alert_count(
            db=db,
            db_session=db_session,
        )

        return db_alert

    # Read

    def get_alert(
        self,
        db: Session,
        alert_id: int,
    ) -> Alert | None:

        return alert_crud.get_alert_by_id(
            db=db,
            alert_id=alert_id,
        )

    def get_all_alerts(
        self,
        db: Session,
    ) -> list[Alert]:

        return alert_crud.get_all_alerts(
            db=db,
        )

    # Update

    def update_alert(
        self,
        db: Session,
        alert_id: int,
        alert_in: AlertUpdate,
    ) -> Alert | None:

        db_alert = alert_crud.get_alert_by_id(
            db=db,
            alert_id=alert_id,
        )

        if db_alert is None:
            return None

        return alert_crud.update_alert(
            db=db,
            db_alert=db_alert,
            alert_in=alert_in,
        )

    # Actions

    def acknowledge_alert(
        self,
        db: Session,
        alert_id: int,
    ) -> Alert | None:

        db_alert = alert_crud.get_alert_by_id(
            db=db,
            alert_id=alert_id,
        )

        if db_alert is None:
            return None

        return alert_crud.acknowledge_alert(
            db=db,
            db_alert=db_alert,
        )

    def dismiss_alert(
        self,
        db: Session,
        alert_id: int,
    ) -> Alert | None:

        db_alert = alert_crud.get_alert_by_id(
            db=db,
            alert_id=alert_id,
        )

        if db_alert is None:
            return None

        return alert_crud.dismiss_alert(
            db=db,
            db_alert=db_alert,
        )


alert_service = AlertService()