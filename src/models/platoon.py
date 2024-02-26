from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Platoon(BaseTable):
    __tablename__ = 'platoon'

    platoon_number: Mapped[intpk]
    vus: Mapped[int]
    semester: Mapped[int] = mapped_column(default=1)
