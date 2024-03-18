from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy_utils import create_view

from models.subject import Subject
from models.grading import Grading
from services.database.view import View
from services.database.connector import BaseTable

gr = aliased(Grading)

subject = (
    (select(Subject.name).select_from(Subject).where(Subject.id == gr.subj_id))
    .scalar_subquery()
    .label("subject")
)
semester = (
    (select(Subject.semester).where(Subject.id == gr.subj_id))
    .scalar_subquery()
    .label("semester")
)
platoon_number = (
    (select(Subject.platoon_id).where(Subject.id == gr.subj_id))
    .scalar_subquery()
    .label("platoon_number")
)


class Marks(BaseTable, View):
    selectable = select(
        gr.mark_date,
        gr.subj_id,
        subject,
        semester,
        platoon_number,
        gr.user_id,
        gr.theme,
        gr.mark,
    )

    __table__ = create_view("marks", selectable, BaseTable.metadata)
