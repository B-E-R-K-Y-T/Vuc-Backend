from datetime import date

from pydantic import BaseModel


class GradingID(BaseModel):
    id: int


class UserGrading(GradingID):
    user_id: int
    mark: int
    mark_date: date
    subj_id: int
    theme: str


class UserGradingDTO(BaseModel):
    user_id: int
    mark: int
    mark_date: date
    subj_id: int
    theme: str


class UpdateGrading(GradingID):
    mark: int
