from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int


class UserCreate(BaseModel):
    name: str
    date_of_birth: datetime
    phone: str
    mail: str
    address: str
    institute: str
    direction_of_study: str
    group_study: str
    platoon_number: int
    squad_number: int
    role: str
    telegram_id: int


class UserCreateResponse(BaseModel):
    token: str
