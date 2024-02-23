from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import schemas.user
from services.database.connector import get_async_session
from services.util import exception_handler
from services.database.worker import DatabaseWorker

router = APIRouter(
    prefix="/users"
)


@router.post("/register",
             description='Регистрация пользователя',
             response_model=schemas.user.UserCreateResponse,
             status_code=HTTPStatus.CREATED)
@exception_handler
async def register(user: schemas.user.UserCreate, session: AsyncSession = Depends(get_async_session)):
    token = await DatabaseWorker.register_user(user, session)

    return {'token': token}
