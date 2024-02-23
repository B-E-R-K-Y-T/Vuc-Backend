from sqlalchemy import Integer, Column, ForeignKey, Date

from services.database.connector import Base
from services.database.table import Table


class Attend(Base, Table):
    __tablename__ = 'attend'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date_v = Column(Date, nullable=False)
    visiting = Column(Integer)
    semester = Column(Integer)
