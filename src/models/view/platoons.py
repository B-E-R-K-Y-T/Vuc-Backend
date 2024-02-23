from sqlalchemy import select, func
from sqlalchemy_utils import create_view

from models.user import User
from models.platoon import Platoon
from services.database.view import View
from services.database.connector import Base

commander = (select(User.name).
             where(User.platoon_number == Platoon.platoon_number and User.role == 'Командир взвода').subquery())
squads = select(func.sum(
    select(1).
    where(User.platoon_number == Platoon.platoon_number and User.squad_number in [1, 2 ,3]).
    group_by(User.squad_number).scalar_subquery())).subquery()


class Platoons(Base, View):
    selectable = select(
        Platoon.vus,
        Platoon.semester,
        commander,
        squads
    )

    __table__ = create_view(
        "platoons",
        selectable,
        Base.metadata
    )
