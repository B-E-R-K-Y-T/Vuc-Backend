from sqlalchemy import select
from sqlalchemy_utils import create_view

from models.user import User
from models.attend import Attend
from services.database.view import View
from services.database.connector import BaseTable

name = (
    (select(User.name).where(User.id == Attend.user_id)).scalar_subquery().label("name")
)
platoon_number = (
    (select(User.platoon_id).where(User.id == Attend.user_id))
    .scalar_subquery()
    .label("platoon_number")
)
squad_number = (
    (select(User.squad_number).where(User.id == Attend.user_id))
    .scalar_subquery()
    .label("squad_number")
)


class Attendance(BaseTable, View):
    selectable = select(
        Attend.date_v,
        Attend.user_id,
        name,
        Attend.visiting,
        platoon_number,
        squad_number,
        Attend.semester,
    )

    __table__ = create_view("attendance", selectable, BaseTable.metadata)
