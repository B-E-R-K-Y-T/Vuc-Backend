from sqlalchemy import Column, Integer, ForeignKey, String

from services.database_connector import Base


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
