import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Attend(BaseTable):
    __tablename__ = "attend"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date_v: Mapped[datetime.date]
    visiting: Mapped[int]
    semester: Mapped[int]
