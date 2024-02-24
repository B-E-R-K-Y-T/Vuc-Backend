from sqlalchemy import select
from sqlalchemy_utils import create_view

from models.user import User
from models.platoon import Platoon
from services.database.view import View
from services.database.connector import Base
from services.auth.auth import Roles

vus = select(Platoon.vus).where(User.platoon_number == Platoon.platoon_number).subquery()


class Students(Base, View):
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
        User.squad_number,
        User.telegram_id,
        User.token,
        User.role
    ).where(User.role != Roles.admin)

    __table__ = create_view(
        "students",
        selectable,
        Base.metadata
    )
