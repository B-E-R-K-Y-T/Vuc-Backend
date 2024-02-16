from sqlalchemy import Column, Integer, String, ForeignKey

from services.database.connector import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String)
    date_of_birth = Column(String)
    mail = Column(String)
    address = Column(String)
    institute = Column(String)
    direction_of_study = Column(String)
    platoon_number = Column(Integer, ForeignKey('platoon.platoon_number'))
    squad_number = Column(Integer)
    role = Column(String, default='Студент')
    telegram_id = Column(Integer)
    token = Column(String)
    group_study = Column(String)


"""
Indexes:
    "student_name" UNIQUE, btree (id) INCLUDE (platoon_number, name)
    "unique_tg_id" UNIQUE CONSTRAINT, btree (telegram_id)
"""
