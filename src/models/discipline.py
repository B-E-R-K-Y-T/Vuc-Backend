import datetime
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class _Type(Enum):
    encouragement = "поощрение"
    penalty = "взыскание"


class Discipline(BaseTable):
    __tablename__ = "discipline"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    type: Mapped[_Type]
    comment: Mapped[str]
    date: Mapped[datetime.date]

    user = relationship("User")
