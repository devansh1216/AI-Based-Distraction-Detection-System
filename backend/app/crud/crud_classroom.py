"""
CRUD operations for the Classroom model.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate


class CRUDClassroom:
    """
    CRUD operations for the Classroom model.
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

        db_classroom = Classroom(
            classroom_code=classroom_in.classroom_code,
            classroom_name=classroom_in.classroom_name,
            floor_number=classroom_in.floor_number,
            building_name=classroom_in.building_name,
            max_capacity=classroom_in.max_capacity,
            is_active=classroom_in.is_active,
        )

        db.add(db_classroom)
        db.commit()
        db.refresh(db_classroom)

        return db_classroom

    # --------------------------------------------------------------------------
    # Read
    # --------------------------------------------------------------------------

    def get_classroom_by_id(
        self,
        db: Session,
        classroom_id: int,
    ) -> Classroom | None:
        """
        Retrieve a classroom by ID.
        """

        statement = select(Classroom).where(
            Classroom.id == classroom_id
        )

        return db.scalar(statement)

    def get_classroom_by_code(
        self,
        db: Session,
        classroom_code: str,
    ) -> Classroom | None:
        """
        Retrieve a classroom by classroom code.
        """

        statement = select(Classroom).where(
            Classroom.classroom_code == classroom_code
        )

        return db.scalar(statement)
    
    def get_all_classrooms(
        self,
        db: Session,
    ) -> list[Classroom]:
        """
        Retrieve all classrooms.
        """

        statement = select(Classroom).order_by(Classroom.id)

        return list(db.scalars(statement).all())

    # --------------------------------------------------------------------------
    # Update
    # --------------------------------------------------------------------------

    def update_classroom(
        self,
        db: Session,
        db_classroom: Classroom,
        classroom_in: ClassroomUpdate,
    ) -> Classroom:
        """
        Update classroom information.
        """

        update_data = classroom_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_classroom, field, value)

        db.commit()
        db.refresh(db_classroom)

        return db_classroom

    # --------------------------------------------------------------------------
    # Activate / Deactivate
    # --------------------------------------------------------------------------

    def activate_classroom(
        self,
        db: Session,
        db_classroom: Classroom,
    ) -> Classroom:
        """
        Activate a classroom.
        """

        db_classroom.is_active = True

        db.commit()
        db.refresh(db_classroom)

        return db_classroom

    def deactivate_classroom(
        self,
        db: Session,
        db_classroom: Classroom,
    ) -> Classroom:
        """
        Deactivate a classroom.
        """

        db_classroom.is_active = False

        db.commit()
        db.refresh(db_classroom)

        return db_classroom


# ------------------------------------------------------------------------------
# Singleton CRUD Instance
# ------------------------------------------------------------------------------

classroom_crud = CRUDClassroom()