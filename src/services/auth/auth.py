from functools import wraps
from http import HTTPStatus
from typing import Callable

from fastapi import HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from config import app_settings, Roles
from models.user import User
from services.auth.manager import get_user_manager

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

SECRET_JWT_KEY = app_settings.SECRET_JWT_KEY


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_JWT_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


class AuthUser(FastAPIUsers):
    def __init__(self, user_manager, auth_backends):
        super().__init__(user_manager, auth_backends)
        self._role_hierarchy = {
            Roles.admin: 4,
            Roles.professor: 3,
            Roles.platoon_commander: 2,
            Roles.squad_commander: 1,
            Roles.student: 0,
        }

    def access_from_admin(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = await func(*args, **kwargs)
            return self._check_role_raise(user, Roles.admin)

        return wrapper

    def access_from_professor(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = await func(*args, **kwargs)
            return self._check_role_raise(user, Roles.professor)

        return wrapper

    def access_from_platoon_commander(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = await func(*args, **kwargs)
            return self._check_role_raise(user, Roles.platoon_commander)

        return wrapper

    def access_from_squad_commander(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = await func(*args, **kwargs)
            return self._check_role_raise(user, Roles.squad_commander)

        return wrapper

    def access_from_student(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = await func(*args, **kwargs)
            return self._check_role_raise(user, Roles.student)

        return wrapper

    def _check_role_raise(self, user: User, role: str) -> User:
        if self._role_hierarchy[user.role] < self._role_hierarchy[role]:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN)

        return user


auth_user = AuthUser(
    get_user_manager,
    [auth_backend],
)


__all__ = ("auth_user", Roles.__name__)
