"""
CRUD operations for the Camera model.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.schemas.camera import CameraCreate, CameraUpdate


class CRUDCamera:
    """
    CRUD operations for the Camera model.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_camera(
        self,
        db: Session,
        camera_in: CameraCreate,
    ) -> Camera:
        """
        Create a new camera.
        """

        db_camera = Camera(
            classroom_id=camera_in.classroom_id,
            camera_name=camera_in.camera_name,
            camera_source=camera_in.camera_source,
            camera_type=camera_in.camera_type,
            resolution=camera_in.resolution,
            fps=camera_in.fps,
            is_active=camera_in.is_active,
        )

        db.add(db_camera)
        db.commit()
        db.refresh(db_camera)

        return db_camera

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_camera_by_id(
        self,
        db: Session,
        camera_id: int,
    ) -> Camera | None:
        """
        Retrieve a camera by ID.
        """

        statement = select(Camera).where(
            Camera.id == camera_id
        )

        return db.scalar(statement)
    
    def get_camera_by_source(
        self,
        db: Session,
        camera_source: str,
    ) -> Camera | None:
        """
        Retrieve a camera by its source.
        """

        statement = select(Camera).where(
            Camera.camera_source == camera_source
        )

        return db.scalar(statement)

    def get_cameras_by_classroom(
        self,
        db: Session,
        classroom_id: int,
    ) -> list[Camera]:
        """
        Retrieve all cameras assigned to a classroom.
        """

        statement = (
            select(Camera)
            .where(Camera.classroom_id == classroom_id)
            .order_by(Camera.id)
        )

        return list(db.scalars(statement).all())
    
    def get_all_cameras(
        self,
        db: Session,
    ) -> list[Camera]:
        """
        Retrieve all cameras.
        """

        statement = select(Camera).order_by(Camera.id)

        return list(db.scalars(statement).all())

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_camera(
        self,
        db: Session,
        db_camera: Camera,
        camera_in: CameraUpdate,
    ) -> Camera:
        """
        Update camera information.
        """

        update_data = camera_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_camera, field, value)

        db.commit()
        db.refresh(db_camera)

        return db_camera

    # --------------------------------------------------------------------------
    # Activate / Deactivate
    # --------------------------------------------------------------------------

    def activate_camera(
        self,
        db: Session,
        db_camera: Camera,
    ) -> Camera:
        """
        Activate a camera.
        """

        db_camera.is_active = True

        db.commit()
        db.refresh(db_camera)

        return db_camera

    def deactivate_camera(
        self,
        db: Session,
        db_camera: Camera,
    ) -> Camera:
        """
        Deactivate a camera.
        """

        db_camera.is_active = False

        db.commit()
        db.refresh(db_camera)

        return db_camera


# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

camera_crud = CRUDCamera()