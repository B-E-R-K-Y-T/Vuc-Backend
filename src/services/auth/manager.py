from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from config import app_settings
from services.auth.database import get_user_db
from models.user import User
from services.logger import LOGGER
from services.util import TokenGenerator, convert_schema_to_dict

USER_SECRET_TOKEN = app_settings.USER_SECRET_TOKEN


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_SECRET_TOKEN
    verification_token_secret = USER_SECRET_TOKEN

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        LOGGER.info(f"User {user.id} has registered.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = convert_schema_to_dict(user_create)

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["token"] = TokenGenerator.generate_new_token()

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
