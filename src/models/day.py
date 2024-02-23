from sqlalchemy import Column, Integer, Date

from services.database.connector import Base
from services.database.table import Table


class Day(Base, Table):
    __tablename__ = 'day'
    date = Column(Date, primary_key=True, nullable=False)
    weekday = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
