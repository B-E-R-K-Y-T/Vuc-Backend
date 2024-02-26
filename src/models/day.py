import datetime

from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import BaseTable


class Day(BaseTable):
    __tablename__ = 'day'

    date: Mapped[datetime.date] = mapped_column(primary_key=True)
    weekday: Mapped[int]
    semester: Mapped[int]
