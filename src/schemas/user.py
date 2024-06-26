from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from fastapi_users import schemas as fastapi_users_schemas

from services.auth.auth import Roles


class _SquadRange(Enum):
    one = 1
    two = 2
    three = 3


class RoleRange(Enum):
    admin = Roles.admin
    professor = Roles.professor
    platoon_commander = Roles.platoon_commander
    squad_commander = Roles.squad_commander
    student = Roles.student


class UserRole(BaseModel):
    role: RoleRange


class UserRead(fastapi_users_schemas.BaseUser[int]):
    id: Optional[int] = None
    email: EmailStr
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    token: str

    class Config:
        from_attributes = True


class UserSelf(UserRead):
    role: RoleRange
    telegram_id: int
    platoon_number: int
    squad_number: _SquadRange


class Student(BaseModel):
    id: int
    name: str
    role: str
    platoon_number: int
    squad_number: _SquadRange
    group_study: str


class UserID(BaseModel):
    id: int


class UserCreate(fastapi_users_schemas.BaseUserCreate):
    name: str
    date_of_birth: datetime
    phone: str
    email: EmailStr
    address: str
    institute: str
    direction_of_study: str
    group_study: str
    platoon_number: int
    squad_number: _SquadRange
    role: RoleRange

    telegram_id: Optional[int]
    password: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserDTO(UserID):
    name: str
    date_of_birth: datetime
    phone: str
    email: EmailStr
    address: str
    institute: str
    direction_of_study: str
    group_study: str
    platoon_number: int
    squad_number: _SquadRange
    role: RoleRange
    telegram_id: int


class EditUser(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    institute: Optional[str] = None
    direction_of_study: Optional[str] = None
    group_study: Optional[str] = None
    platoon_number: Optional[int] = None
    squad_number: Optional[_SquadRange] = None
    telegram_id: Optional[int] = None


class UserSetAttr(UserID):
    data: EditUser


class UserSetMail(UserID):
    email: EmailStr


class UserSetTelegramID(UserID):
    telegram_id: int
