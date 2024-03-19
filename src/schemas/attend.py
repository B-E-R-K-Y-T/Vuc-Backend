from datetime import date
from typing import Optional

from pydantic import BaseModel


class AttendID(BaseModel):
    id: int


class AttendCreate(BaseModel):
    user_id: int
    date_v: date
    visiting: int
    semester: int
    confirmed: Optional[bool] = False


class ConfirmationAttend(AttendID):
    confirmed: Optional[bool] = False


class AttendDTO(AttendID, AttendCreate):
    pass
