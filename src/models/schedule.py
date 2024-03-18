from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Schedule(BaseTable):
    __tablename__ = "schedule"

    id: Mapped[intpk]
    aud: Mapped[str]
    platoon_number: Mapped[int] = mapped_column(ForeignKey("platoon.platoon_number"))
    day_id: Mapped[datetime.date] = mapped_column(ForeignKey("day.id"))

    platoon = relationship("Platoon", back_populates="schedule")
    day = relationship("Day", back_populates="schedule")
