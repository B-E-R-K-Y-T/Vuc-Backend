from sqlalchemy import select, func
from sqlalchemy_utils import create_view

from models.subject import Subject
from models.grading import Grading
from services.database.base_view import View
from services.database.connector import Base

subject = select(Subject.name).where(Subject.id == Grading.id).subquery()
semester = select(Subject.semester).where(Subject.id == Grading.subj_id).subquery()
platoon_number = select(Subject.platoon_id).where(Subject.id == Grading.subj_id).subquery()


class Marks(Base, View):
    selectable = select(
        func.to_char(Grading.mark_date, 'DD/MM/YYYY').label('mark_date'),
        Grading.subj_id,
        subject,
        semester,
        platoon_number,
        Grading.user_id,
        Grading.theme,
        Grading.mark
    )

    __table__ = create_view(
        "marks",
        selectable,
        Base.metadata
    )
