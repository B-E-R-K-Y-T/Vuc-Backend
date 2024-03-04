from datetime import date

from pydantic import BaseModel


class AttendID(BaseModel):
    id: int


class AttendDTO(AttendID):
    user_id: int
    date_v: date
    visiting: int
    semester: int
    confirmed: bool
