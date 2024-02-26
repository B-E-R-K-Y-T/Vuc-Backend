from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Subject(BaseTable):
    __tablename__ = 'subject'

    id: Mapped[intpk]
    platoon_id: Mapped[int] = mapped_column(ForeignKey('platoon.platoon_number'))
    semester: Mapped[int]
    admin_id: Mapped[int]
    name: Mapped[str]
