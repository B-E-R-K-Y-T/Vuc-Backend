from sqlalchemy import select, func
from sqlalchemy_utils import create_view

from models.user import User
from models.attend import Attend
from services.database.base_view import View
from services.database.connector import Base

name = select(User.name).where(User.id == Attend.user_id).subquery()
platoon_number = select(User.platoon_number).where(User.id == Attend.user_id).subquery()
squad_number = select(User.squad_number).where(User.id == Attend.user_id).subquery()


class Attendance(Base, View):
    selectable = select(
        func.to_char(Attend.date_v, 'DD/MM/YYYY').label('date_v'),
        Attend.user_id,
        name,
        Attend.visiting,
        platoon_number,
        squad_number,
        Attend.semester
    )

    __table__ = create_view(
        "attendance",
        selectable,
        Base.metadata
    )
