from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Platoon(BaseTable):
    __tablename__ = "platoon"

    id: Mapped[intpk]
    platoon_number: Mapped[int] = mapped_column(unique=True)
    vus: Mapped[int]
    semester: Mapped[int] = mapped_column(default=1)
