import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class User(SQLAlchemyBaseUserTable[int], BaseTable):
    __tablename__ = "user"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    address: Mapped[str]
    institute: Mapped[str]
    direction_of_study: Mapped[str]
    platoon_id: Mapped[int] = mapped_column(ForeignKey("platoon.id"))
    squad_number: Mapped[int]
    role: Mapped[str] = mapped_column(default="Студент")
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    token: Mapped[str]
    group_study: Mapped[str]
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    registered_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow()
    )
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    attend = relationship('Attend', back_populates='user', uselist=False)
    grading = relationship('Grading', back_populates='user')
    message_queue = relationship('MessageQueue', back_populates='user')
    platoon = relationship('Platoon', back_populates='user', uselist=False)

    __table_args__ = (
        CheckConstraint("squad_number IN (1, 2, 3)", name="squad_number_check_c"),
    )
