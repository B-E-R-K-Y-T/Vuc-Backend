from sqlalchemy import Column, Integer, String, ForeignKey

from services.database.connector import Base
from services.database.table import Table


class Subject(Base, Table):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    platoon_id = Column(Integer, ForeignKey('platoon.platoon_number'), nullable=False)
    semester = Column(Integer, nullable=False)
    admin_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
