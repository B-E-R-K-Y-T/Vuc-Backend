import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_type import intpk
from services.database.table import Table


class Attend(Base, Table):
    __tablename__ = 'attend'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date_v: Mapped[datetime.date]
    visiting: Mapped[int]
    semester: Mapped[int]
