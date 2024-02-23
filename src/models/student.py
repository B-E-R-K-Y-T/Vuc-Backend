from sqlalchemy import Column, Integer, String, Date

from services.database.connector import Base


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(String)
    date_of_birth = Column(Date)
    mail = Column(String)
    address = Column(String)
    institute = Column(String)
    direction_of_study = Column(String)
    group_study = Column(String)
    platoon_number = Column(Integer)
    vus = Column(Integer)
    squad_number = Column(Integer)
    telegram_id = Column(Integer)
    token = Column(String)
    role = Column(String)
