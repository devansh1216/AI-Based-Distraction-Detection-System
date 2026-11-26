"""
Business logic for classroom management.
"""

from sqlalchemy.orm import Session

from app.crud.crud_classroom import classroom_crud
from app.models.classroom import Classroom
from app.schemas.classroom import (
    ClassroomCreate,
    ClassroomUpdate,
)


class ClassroomService:
    """
    Business logic for classroom management.
    """

    # --------------------------------------------------------------------------
    # Create
    # --------------------------------------------------------------------------

    def create_classroom(
        self,
        db: Session,
        classroom_in: ClassroomCreate,
    ) -> Classroom:
        """
        Create a new classroom.
        """

        existing_classroom = classroom_crud.get_classroom_by_code(
            db=db,
            classroom_code=classroom_in.classroom_code,
        )

        if existing_classroom is not None:
            raise ValueError("Classroom code already exists.")

        return classroom_crud.create_classroom(
            db=db,
            classroom_in=classroom_in,
        )

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_classroom(
        self,
        db: Session,
        classroom_id: int,
    ) -> Classroom | None:
        """
        Retrieve a classroom by ID.
        """

        db_classroom = classroom_crud.get_classroom_by_id(
            db=db,
            classroom_id=classroom_id,
        )

        return db_classroom

    def get_all_classrooms(
        self,
        db: Session,
    ) -> list[Classroom]:
        """
        Retrieve all classrooms.
        """

        return classroom_crud.get_all_classrooms(
            db=db,
        )

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_classroom(
        self,
        db: Session,
        classroom_id: int,
        classroom_in: ClassroomUpdate,
    ) -> Classroom | None:
        """
        Update classroom information.
        """

        db_classroom = classroom_crud.get_classroom_by_id(
            db=db,
            classroom_id=classroom_id,
        )

        if db_classroom is None:
            return None

        if (
            classroom_in.classroom_code is not None
            and classroom_in.classroom_code != db_classroom.classroom_code
        ):
            existing_classroom = classroom_crud.get_classroom_by_code(
                db=db,
                classroom_code=classroom_in.classroom_code,
            )

            if existing_classroom is not None:
                raise ValueError("Classroom code already exists.")

        return classroom_crud.update_classroom(
            db=db,
            db_classroom=db_classroom,
            classroom_in=classroom_in,
        )

    # --------------------------------------------------------------------------
    # Activate / Deactivate
    # --------------------------------------------------------------------------

    def activate_classroom(
        self,
        db: Session,
        classroom_id: int,
    ) -> Classroom | None:
        """
        Activate a classroom.
        """

        db_classroom = classroom_crud.get_classroom_by_id(
            db=db,
            classroom_id=classroom_id,
        )

        if db_classroom is None:
            return None

        return classroom_crud.activate_classroom(
            db=db,
            db_classroom=db_classroom,
        )

    def deactivate_classroom(
        self,
        db: Session,
        classroom_id: int,
    ) -> Classroom | None:
        """
        Deactivate a classroom.
        """

        db_classroom = classroom_crud.get_classroom_by_id(
            db=db,
            classroom_id=classroom_id,
        )
    
        if db_classroom is None:
            return None
        
        return classroom_crud.deactivate_classroom(
            db=db,
            db_classroom=db_classroom,
        )


# ------------------------------------------------------------------------------
# Singleton Service Instance
# ------------------------------------------------------------------------------

classroom_service = ClassroomService()