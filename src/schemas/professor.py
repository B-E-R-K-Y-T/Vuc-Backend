from pydantic import BaseModel


class SubjectID(BaseModel):
    id: int


class MarkID(BaseModel):
    id: int


# class MarkDTO(BaseModel):
#


class SubjectDTO(SubjectID):
    platoon_id: int
    semester: int
    admin_id: int
    name: str


class ProfessorID(BaseModel):
    id: int


class Semesters(BaseModel):
    semesters: list
