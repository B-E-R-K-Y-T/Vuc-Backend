from sqlalchemy import select, func
from sqlalchemy_utils import create_view

from models.user import User
from models.platoon import Platoon
from services.database.view import View
from services.database.connector import Base
from services.auth.auth import Roles

commander = (select(User.name).
             where(User.platoon_number == Platoon.platoon_number,
                   User.role == Roles.platoon_commander).subquery())
squads = (select(
    func.sum(1)).
          select_from(select(User.squad_number).
                      where(User.platoon_number == Platoon.platoon_number,
                            User.squad_number.in_([1, 2, 3])).
                      group_by(User.squad_number).subquery()
                      )
          ).subquery()


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
