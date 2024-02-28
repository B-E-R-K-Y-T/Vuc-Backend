from sqlalchemy import select, func, and_
from sqlalchemy_utils import create_view
from sqlalchemy.orm import aliased

from models.user import User
from models.platoon import Platoon
from services.database.view import View
from services.database.connector import BaseTable
from config import Roles


commander = (
    select(User.name).
    where(
        and_(
            User.platoon_number == Platoon.platoon_number,
            User.role == Roles.platoon_commander
        )
    )
).correlate(Platoon).label('commander')

squads = (
    select(
        func.sum(1).label('sum')
    ).
    select_from(
        select(1).
        where(
            and_(
                User.platoon_number == Platoon.platoon_number,
                User.squad_number.in_([1, 2, 3])
            )
        ).
        group_by(User.squad_number).correlate(Platoon).subquery()
    )
).correlate(Platoon).label('squads')


class Platoons(BaseTable, View):
    selectable = select(
        Platoon.platoon_number,
        Platoon.vus,
        Platoon.semester,
        commander,
        squads
    )

    __table__ = create_view(
        "platoons",
        selectable,
        BaseTable.metadata
    )
