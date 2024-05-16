from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SubjectID(BaseModel):
    id: int


class MarkID(BaseModel):
    id: int


class SubjectDTO(SubjectID):
    platoon_id: int
    semester: int
    admin_id: int
    name: str


class ProfessorID(BaseModel):
    id: int


class Professor(ProfessorID):
    name: str


class Semesters(BaseModel):
    semesters: list


class Gradings(BaseModel):
    id: int
    mark: int
    mark_date: date
    theme: str


class Visit(Enum):
    zero = 0  # не был
    one = 1  # был
    two = 2  # наряд
    three = 3  # командировка
    four = 4  # болезнь


class AttendanceDTO(BaseModel):
    date_v: date
    visiting: Visit
    user_id: int


class AttendancePlatoon(BaseModel):
    date_v: date
    visiting: Visit
    platoon_number: int
    semester: Optional[int] = None
