import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class Grading(BaseTable):
    __tablename__ = "grading"

    id: Mapped[intpk]
    subj_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    mark: Mapped[int]
    mark_date: Mapped[datetime.date]
    theme: Mapped[str]

    subject = relationship("Subject", back_populates="grading")
    user = relationship("User", back_populates="grading")
