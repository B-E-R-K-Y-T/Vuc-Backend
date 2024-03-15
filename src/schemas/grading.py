from datetime import date

from pydantic import BaseModel


class UserMark(BaseModel):
    user_id: int
    id: int
    mark: int
    mark_date: date
    subj_id: int
    theme: str
