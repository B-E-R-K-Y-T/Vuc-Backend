from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import TelegramIDError
from schemas.user import UserRole, UserRead, UserSetAttr, UserSetMail, UserSetTelegramID
from services.auth.auth import auth_user
from services.database.connector import get_async_session
from services.util import exception_handler, convert_schema_to_dict
from services.database.worker import DatabaseWorker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/users",
    dependencies=[Depends(auth_user.access_from_student(current_user))]
)


@router.get("/get_user_role",
            description='Получить роль пользователя',
            response_model=UserRole,
            status_code=HTTPStatus.OK)
@exception_handler
async def get_user_role(user_id: int, session: AsyncSession = Depends(get_async_session)):
    role = await DatabaseWorker(session).get_user_role(user_id)

    return {'role': role}


@router.get("/get_user",
            description='Получить пользователя',
            response_model=UserRead,
            status_code=HTTPStatus.OK)
@exception_handler
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await DatabaseWorker(session).get_user(user_id)

    return UserRead.model_validate(user, from_attributes=True)


@router.get("/get_user_by_tg",
            description='Получить пользователя по его телеграм id',
            response_model=UserRead,
            status_code=HTTPStatus.OK)
@exception_handler
async def get_user_by_tg(telegram_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await DatabaseWorker(session).get_user_by_tg(telegram_id)

    return UserRead.model_validate(user, from_attributes=True)


@router.post("/set_user_attr",
             description='Установить атрибут(ы) пользователя в некоторое значение',
             status_code=HTTPStatus.NO_CONTENT)
@exception_handler
async def set_user_attr(attrs: UserSetAttr, session: AsyncSession = Depends(get_async_session)):
    data = {attr: value for attr, value in convert_schema_to_dict(attrs.data).items() if value is not None}
    await DatabaseWorker(session).set_user_attr(attrs.id, **data)


@router.post("/set_user_mail",
             description='Установить почту пользователя в некоторое значение',
             status_code=HTTPStatus.NO_CONTENT)
@exception_handler
async def set_user_email(u_email: UserSetMail, session: AsyncSession = Depends(get_async_session)):
    if await DatabaseWorker(session).email_is_exist(u_email.email):
        raise TelegramIDError(
            message=f'Email {u_email.email} already exists.',
            status_code=HTTPStatus.BAD_REQUEST
        )

    await DatabaseWorker(session).set_user_attr(u_email.id, email=u_email.email)


@router.post("/set_user_telegram_id",
             description='Установить телеграм id пользователя в некоторое значение',
             status_code=HTTPStatus.NO_CONTENT)
@exception_handler
async def set_user_telegram_id(u_telegram_id: UserSetTelegramID, session: AsyncSession = Depends(get_async_session)):
    if await DatabaseWorker(session).telegram_id_is_exist(u_telegram_id.telegram_id):
        raise TelegramIDError(
            message=f'Telegram ID {u_telegram_id.telegram_id} already exists.',
            status_code=HTTPStatus.BAD_REQUEST
        )

    await DatabaseWorker(session).set_user_attr(u_telegram_id.id, telegram_id=u_telegram_id.telegram_id)
