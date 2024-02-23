from sqlalchemy import Column, Integer, String, ForeignKey

from services.database.connector import Base
from services.database.table import Table


class MessageQueue(Base, Table):
    __tablename__ = 'message_queue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, ForeignKey('user.telegram_id'), nullable=False)
    message = Column(String, nullable=False)
