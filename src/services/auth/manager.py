from http import HTTPStatus
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from sqlalchemy.ext.asyncio import AsyncSession

from config import app_settings
from exceptions import PlatoonError
from services.auth.database import get_user_db
from models.user import User
from services.database.connector import get_async_session
from services.database.worker import DatabaseWorker
from services.logger import LOGGER
from services.util import TokenGenerator, convert_schema_to_dict

USER_SECRET_TOKEN = app_settings.AUTH_USER_SECRET_TOKEN


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_SECRET_TOKEN
    verification_token_secret = USER_SECRET_TOKEN

    def __init__(self, *args, session: AsyncSession = Depends(get_async_session), **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        LOGGER.info(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)

        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        if await DatabaseWorker(self.session).platoon_commander_is_exist(user_create.platoon_number):
            raise PlatoonError(
                f"Взвод {user_create.platoon_number} уже имеет командира!",
                status_code=HTTPStatus.BAD_REQUEST
            )

        user_dict = convert_schema_to_dict(user_create)

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["token"] = TokenGenerator.generate_new_token()

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db), session: AsyncSession = Depends(get_async_session)):
    yield UserManager(user_db, session=session)
