from sqlalchemy import Column, Integer, String

from services.database.connector import Base
from services.database.table import Table


class Admin(Base, Table):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
