import datetime

from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_types import intpk
from services.database.table import Table


class Student(Base, Table):
    __tablename__ = 'student'

    id: Mapped[intpk]
    name: Mapped[str]
    phone: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    mail: Mapped[str]
    address: Mapped[str]
    institute: Mapped[str]
    direction_of_study: Mapped[str]
    group_study: Mapped[str]
    platoon_number: Mapped[int]
    vus: Mapped[int]
    squad_number: Mapped[int]
    telegram_id: Mapped[int]
    token: Mapped[str]
    role: Mapped[str]
