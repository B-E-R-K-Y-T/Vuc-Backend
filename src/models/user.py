import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_type import intpk
from services.database.table import Table


class User(SQLAlchemyBaseUserTable[int], Base, Table):
    __tablename__ = 'user'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    address: Mapped[str]
    institute: Mapped[str]
    direction_of_study: Mapped[str]
    platoon_number: Mapped[int] = mapped_column(ForeignKey('platoon.platoon_number'))
    squad_number: Mapped[int]
    role: Mapped[str] = mapped_column(default='Студент')
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    token: Mapped[str]
    group_study: Mapped[str]
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    # password: Mapped[str] = mapped_column(nullable=True)
    registered_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
