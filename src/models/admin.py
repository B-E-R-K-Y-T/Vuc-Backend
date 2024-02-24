from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_type import intpk
from services.database.table import Table


class Admin(Base, Table):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
