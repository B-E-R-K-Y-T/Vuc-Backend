from sqlalchemy import select
from sqlalchemy_utils import create_view

from models.subject import Subject
from models.grading import Grading
from services.database.view import View
from services.database.connector import BaseTable

subject = select(Subject.name).where(Subject.id == Grading.id).subquery()
semester = select(Subject.semester).where(Subject.id == Grading.subj_id).subquery()
platoon_number = select(Subject.platoon_id).where(Subject.id == Grading.subj_id).subquery()


class Marks(BaseTable, View):
    selectable = select(
        Grading.mark_date,
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
        BaseTable.metadata
    )
