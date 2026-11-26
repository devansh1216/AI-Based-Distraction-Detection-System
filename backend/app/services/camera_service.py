"""
Business logic for camera management.
"""

from sqlalchemy.orm import Session

from app.crud.crud_camera import camera_crud
from app.crud.crud_classroom import classroom_crud
from app.models.camera import Camera
from app.schemas.camera import (
    CameraCreate,
    CameraUpdate,
)


class CameraService:
    """
    Business logic for camera management.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_camera(
        self,
        db: Session,
        camera_in: CameraCreate,
    ) -> Camera:
        
        db_classroom = classroom_crud.get_classroom_by_id(
            db=db,
            classroom_id=camera_in.classroom_id,
        )

        if db_classroom is None:
            raise ValueError("Classroom not found.")

        existing_camera = camera_crud.get_camera_by_source(
            db=db,
            camera_source=camera_in.camera_source,
        )

        if existing_camera is not None:
            raise ValueError("Camera source already exists.")

        return camera_crud.create_camera(
            db=db,
            camera_in=camera_in,
        )

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_camera(
        self,
        db: Session,
        camera_id: int,
    ) -> Camera | None:
        
        return camera_crud.get_camera_by_id(
            db=db,
            camera_id=camera_id,
        )

    def get_all_cameras(
        self,
        db: Session,
    ) -> list[Camera]:
        
        return camera_crud.get_all_cameras(
            db=db,
        )

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_camera(
        self,
        db: Session,
        camera_id: int,
        camera_in: CameraUpdate,
    ) -> Camera | None:
        
        db_camera = camera_crud.get_camera_by_id(
            db=db,
            camera_id=camera_id,
        )

        if db_camera is None:
            return None

        if (
            camera_in.classroom_id is not None
        ):
            classroom = classroom_crud.get_classroom_by_id(
                db=db,
                classroom_id=camera_in.classroom_id,
            )

            if classroom is None:
                raise ValueError("Classroom not found.")

        if (
            camera_in.camera_source is not None
            and camera_in.camera_source != db_camera.camera_source
        ):
            existing_camera = camera_crud.get_camera_by_source(
                db=db,
                camera_source=camera_in.camera_source,
            )

            if existing_camera is not None:
                raise ValueError("Camera source already exists.")

        return camera_crud.update_camera(
            db=db,
            db_camera=db_camera,
            camera_in=camera_in,
        )

    # --------------------------------------------------------------------------
    # Activate / Deactivate
    # --------------------------------------------------------------------------

    def activate_camera(
        self,
        db: Session,
        camera_id: int,
    ) -> Camera | None:
        
        db_camera = camera_crud.get_camera_by_id(
            db=db,
            camera_id=camera_id,
        )

        if db_camera is None:
            return None

        return camera_crud.activate_camera(
            db=db,
            db_camera=db_camera,
        )

    def deactivate_camera(
        self,
        db: Session,
        camera_id: int,
    ) -> Camera | None:
        
        db_camera = camera_crud.get_camera_by_id(
            db=db,
            camera_id=camera_id,
        )

        if db_camera is None:
            return None

        return camera_crud.deactivate_camera(
            db=db,
            db_camera=db_camera,
        )


camera_service = CameraService()