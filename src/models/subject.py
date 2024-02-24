from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_type import intpk
from services.database.table import Table


class Subject(Base, Table):
    __tablename__ = 'subject'

    id: Mapped[intpk]
    platoon_id: Mapped[int] = mapped_column(ForeignKey('platoon.platoon_number'))
    semester: Mapped[int]
    admin_id: Mapped[int]
    name: Mapped[str]
