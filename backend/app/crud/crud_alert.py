"""
CRUD operations for the Alert model.
"""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.alert import AlertStatus
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate


class CRUDAlert:
    """
    CRUD operations for the Alert model.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_alert(
        self,
        db: Session,
        alert_in: AlertCreate,
    ) -> Alert:
        """
        Create a new alert.
        """

        db_alert = Alert(
            session_id=alert_in.session_id,
            tracking_id=alert_in.tracking_id,
            alert_type=alert_in.alert_type,
            severity=alert_in.severity,
            status=alert_in.status,
            generated_at=alert_in.generated_at,
            acknowledged_at=alert_in.acknowledged_at,
        )

        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)

        return db_alert

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_alert_by_id(
        self,
        db: Session,
        alert_id: int,
    ) -> Alert | None:
        """
        Retrieve an alert by ID.
        """

        statement = select(Alert).where(
            Alert.id == alert_id
        )

        return db.scalar(statement)

    def get_alerts_by_session(
        self,
        db: Session,
        session_id: int,
    ) -> list[Alert]:
        """
        Retrieve all alerts for a monitoring session.
        """

        statement = (
            select(Alert)
            .where(Alert.session_id == session_id)
            .order_by(Alert.generated_at.desc())
        )

        return list(db.scalars(statement).all())

    def get_active_alerts(
        self,
        db: Session,
    ) -> list[Alert]:
        """
        Retrieve all active alerts.
        """

        statement = (
            select(Alert)
            .where(Alert.status == AlertStatus.ACTIVE)
            .order_by(Alert.generated_at.desc())
        )

        return list(db.scalars(statement).all())
    
    def get_all_alerts(
        self,
        db: Session,
    ) -> list[Alert]:
        """
        Retrieve all alerts.
        """

        statement = (
            select(Alert)
            .order_by(Alert.generated_at.desc())
        )

        return list(db.scalars(statement).all())

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_alert(
        self,
        db: Session,
        db_alert: Alert,
        alert_in: AlertUpdate,
    ) -> Alert:
        """
        Update alert information.
        """

        update_data = alert_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_alert, field, value)

        db.commit()
        db.refresh(db_alert)

        return db_alert

    # --------------------------------------------------------------------------
    # Alert Actions
    # --------------------------------------------------------------------------

    def acknowledge_alert(
        self,
        db: Session,
        db_alert: Alert,
    ) -> Alert:
        """
        Mark an alert as acknowledged.
        """

        db_alert.status = AlertStatus.ACKNOWLEDGED
        db_alert.acknowledged_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_alert)

        return db_alert

    def dismiss_alert(
        self,
        db: Session,
        db_alert: Alert,
    ) -> Alert:
        """
        Mark an alert as dismissed.
        """

        db_alert.status = AlertStatus.DISMISSED
        db_alert.acknowledged_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_alert)

        return db_alert


# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

alert_crud = CRUDAlert()