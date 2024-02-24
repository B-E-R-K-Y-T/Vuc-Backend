import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_type import intpk, RolesRange
from services.database.table import Table


class User(Base, Table):
    __tablename__ = 'user'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    mail: Mapped[str]
    address: Mapped[str]
    institute: Mapped[str]
    direction_of_study: Mapped[str]
    platoon_number: Mapped[int] = mapped_column(ForeignKey('platoon.platoon_number'))
    squad_number: Mapped[int]
    role: Mapped[RolesRange] = mapped_column(default='Студент')
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    token: Mapped[str]
    group_study: Mapped[str]
