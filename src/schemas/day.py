import datetime

from pydantic import BaseModel


class DayId(BaseModel):
    id: int


class DayCreate(BaseModel):
    date: datetime.date
    weekday: int
    semester: int
    holiday: bool


class DayDTO(DayCreate, DayId):
    pass
