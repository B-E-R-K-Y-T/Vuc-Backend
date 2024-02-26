from sqlalchemy import select
from sqlalchemy_utils import create_view

from models.user import User
from models.platoon import Platoon
from services.database.view import View
from services.database.connector import BaseTable

vus = select(Platoon.vus).where(User.platoon_number == Platoon.platoon_number).subquery()
course_number = select(Platoon.semester).where(User.platoon_number == Platoon.platoon_number).subquery()


class Users(BaseTable, View):
    selectable = select(
        User.name,
        User.id,
        User.phone,
        User.date_of_birth,
        User.email,
        User.address,
        User.institute,
        User.direction_of_study,
        User.group_study,
        User.platoon_number,
        vus,
        course_number,
        User.squad_number,
        User.telegram_id,
        User.token,
        User.role
    )

    __table__ = create_view(
        "users",
        selectable,
        BaseTable.metadata
    )
