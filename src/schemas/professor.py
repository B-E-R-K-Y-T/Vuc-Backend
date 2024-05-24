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
    was_not = 0  # не был
    was = 1  # был
    attire = 2  # наряд
    secondment = 3  # командировка
    disease = 4  # болезнь


class AttendanceDTO(BaseModel):
    date_v: date
    visiting: Visit
    user_id: int


class AttendanceReplace(BaseModel):
    attend_id: int
    visiting: Visit


class AttendancePlatoon(BaseModel):
    date_v: date
    visiting: Visit
    platoon_number: int
    semester: Optional[int] = None
