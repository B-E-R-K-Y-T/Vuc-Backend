import datetime

from pydantic import BaseModel

from models.discipline import _Type


class DisciplineId(BaseModel):
    id: int


class DisciplineCreate(BaseModel):
    date: datetime.date
    user_id: int
    type: _Type
    comment: str
    date: datetime.date


class DaDisciplineDTO(DisciplineCreate, DisciplineId):
    pass
