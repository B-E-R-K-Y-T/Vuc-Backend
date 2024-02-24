import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_type import intpk
from services.database.table import Table


class Grading(Base, Table):
    __tablename__ = 'grading'

    id: Mapped[intpk]
    subj_id: Mapped[int] = mapped_column(ForeignKey('subject.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    mark: Mapped[int]
    mark_date: Mapped[datetime.date]
    theme: Mapped[str]
