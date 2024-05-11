from http import HTTPStatus
from typing import Optional, TYPE_CHECKING

from fastapi import Depends, Request
from fastapi.openapi.models import Response
from fastapi_users import BaseUserManager, IntegerIDMixin, models
from sqlalchemy.ext.asyncio import AsyncSession

from config import app_settings, Roles
from exceptions import PlatoonError, UserAlreadyExists
from services.auth.database import get_user_db
from models.user import User
from services.database.connector import get_async_session
from services.database.worker import DatabaseWorker
from services.logger import LOGGER
from services.util import TokenGenerator, convert_schema_to_dict

if TYPE_CHECKING:
    from schemas.user import UserCreate

USER_SECRET_TOKEN = app_settings.AUTH_USER_SECRET_TOKEN


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_SECRET_TOKEN
    verification_token_secret = USER_SECRET_TOKEN

    def __init__(
        self, *args, session: AsyncSession = Depends(get_async_session), **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.session = session

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        LOGGER.info(f"User {user.id} has registered.")

    async def on_after_login(
        self,
        user: models.UP,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        LOGGER.info(f"User {user.id} has login.")

    async def create(
        self,
        user_create: "UserCreate",
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)

        if existing_user is not None:
            raise UserAlreadyExists(
                message=f"User {user_create.email} already exists."
            )

        if user_create.role.value == Roles.platoon_commander:
            if await DatabaseWorker(self.session).platoon_commander_is_exist(
                user_create.platoon_number
            ):
                raise PlatoonError(
                    f"The platoon {user_create.platoon_number} already has a commander!",
                    status_code=HTTPStatus.BAD_REQUEST,
                )

        if not await DatabaseWorker(self.session).platoon_number_is_exist(user_create.platoon_number):
            raise PlatoonError(
                message=f"Platoon number: {user_create.platoon_number} not found",
                status_code=HTTPStatus.NOT_FOUND,
            )

        user_dict = convert_schema_to_dict(user_create)

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["token"] = TokenGenerator.generate_new_token()

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(
    user_db=Depends(get_user_db), session: AsyncSession = Depends(get_async_session)
):
    yield UserManager(user_db, session=session)
