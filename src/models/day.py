import datetime

from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.table import Table


class Day(Base, Table):
    __tablename__ = 'day'

    date: Mapped[datetime.date] = mapped_column(primary_key=True)
    weekday: Mapped[int]
    semester: Mapped[int]
