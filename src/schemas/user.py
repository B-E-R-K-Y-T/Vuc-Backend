from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from fastapi_users import schemas

from services.auth.auth import Roles


class SquadRange(Enum):
    one = 1
    two = 2
    three = 3


class RoleRange(Enum):
    admin = Roles.admin
    professor = Roles.professor
    platoon_commander = Roles.platoon_commander
    squad_commander = Roles.squad_commander
    student = Roles.student


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    token: str

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int


class UserCreate(schemas.BaseUserCreate):
    name: str
    date_of_birth: datetime
    phone: str
    email: EmailStr
    address: str
    institute: str
    direction_of_study: str
    group_study: str
    platoon_number: int
    squad_number: SquadRange
    role: RoleRange
    telegram_id: int

    password: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreateResponse(BaseModel):
    token: str
