from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from services.database.connector import Base
from services.database.db_types import intpk
from services.database.table import Table


class MessageQueue(Base, Table):
    __tablename__ = 'message_queue'

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    message: Mapped[str]
