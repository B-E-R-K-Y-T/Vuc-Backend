from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.database.connector import BaseTable
from services.database.db_types import intpk


class MessageQueue(BaseTable):
    __tablename__ = "message_queue"

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(ForeignKey("user.telegram_id"))
    message: Mapped[str]

    user = relationship("User", back_populates="message_queue", uselist=False)
