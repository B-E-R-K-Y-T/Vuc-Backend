"""

CREATE VIEW vuc.platoons AS
 SELECT platoon_number,
    vus,
    semester,
    ( SELECT "user".name
           FROM vuc."user"
          WHERE (("user".platoon_number = pl.platoon_number) AND (("user".role)::text = 'Командир взвода'::text))) AS commander,
    ( SELECT sum(1) AS sum
           FROM ( SELECT 1 AS "?column?"
                   FROM vuc."user"
                  WHERE (("user".platoon_number = pl.platoon_number) AND (ARRAY["user".squad_number] <@ ARRAY[1, 2, 3]))
                  GROUP BY "user".squad_number) unnamed_subquery) AS squads
   FROM vuc.platoon pl;


"""
from sqlalchemy import select, func
from sqlalchemy_utils import create_view

from models.user import User
from models.platoon import Platoon
from services.database.base_view import View
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
