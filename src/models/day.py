from sqlalchemy import Column, Integer, Date

from services.database.connector import Base


class Day(Base):
    __tablename__ = 'day'
    date = Column(Date, primary_key=True, nullable=False)
    weekday = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
