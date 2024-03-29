from sqlalchemy import Column, Integer

from services.database.connector import Base


class Platoon(Base):
    __tablename__ = 'platoon'
    platoon_number = Column(Integer, primary_key=True, autoincrement=True)
    vus = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False, default=1)
