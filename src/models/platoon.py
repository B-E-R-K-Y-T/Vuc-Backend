from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_type import intpk
from services.database.table import Table


class Platoon(Base, Table):
    __tablename__ = 'platoon'

    platoon_number: Mapped[intpk]
    vus: Mapped[int]
    semester: Mapped[int] = mapped_column(default=1)
