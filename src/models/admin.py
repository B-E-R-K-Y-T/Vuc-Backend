from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Admin(BaseTable):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
