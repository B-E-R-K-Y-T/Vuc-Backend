from sqlalchemy import Column, Integer, Date, String, ForeignKey

from services.database.connector import Base
from services.database.table import Table


class Grading(Base, Table):
    __tablename__ = 'grading'
    id = Column(Integer, autoincrement=True, primary_key=True)
    subj_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    mark = Column(Integer, nullable=False)
    mark_date = Column(Date, nullable=False)
    theme = Column(String)
