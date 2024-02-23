from sqlalchemy import Column, Integer, String, ForeignKey, Date

from services.database.connector import Base
from services.database.table import Table


class User(Base, Table):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String)
    date_of_birth = Column(Date)
    mail = Column(String)
    address = Column(String)
    institute = Column(String)
    direction_of_study = Column(String)
    platoon_number = Column(Integer, ForeignKey('platoon.platoon_number'))
    squad_number = Column(Integer)
    role = Column(String, default='Студент')
    telegram_id = Column(Integer, unique=True, nullable=False)
    token = Column(String)
    group_study = Column(String)
