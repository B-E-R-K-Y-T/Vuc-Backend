from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Platoon(BaseTable):
    __tablename__ = "platoon"

    platoon_number: Mapped[int] = mapped_column(primary_key=True)
    vus: Mapped[int]
    semester: Mapped[int] = mapped_column(default=1)

    schedule = relationship("Schedule", back_populates="platoon")
    subject = relationship("Subject", back_populates="platoon")
    user = relationship("User", back_populates="platoon")
