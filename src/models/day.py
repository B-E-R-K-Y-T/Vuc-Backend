import datetime

from sqlalchemy.orm import Mapped, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Day(BaseTable):
    __tablename__ = "day"

    id: Mapped[intpk]
    date: Mapped[datetime.date]
    weekday: Mapped[int]
    semester: Mapped[int]
    holiday: Mapped[bool]

    schedule = relationship("Schedule", back_populates="day")
