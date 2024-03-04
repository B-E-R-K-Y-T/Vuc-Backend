from http import HTTPStatus

from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import TelegramIDError, EmailError, UserNotFound
from schemas.attend import AttendDTO
from schemas.user import (
    UserRole,
    UserRead,
    UserSetAttr,
    UserSetMail,
    UserSetTelegramID,
    UserID,
    Student,
)
from services.auth.auth import auth_user
from services.database.connector import get_async_session
from services.util import exception_handler, convert_schema_to_dict
from services.database.worker import DatabaseWorker

current_user = auth_user.current_user()
router = APIRouter(
    prefix='/users', dependencies=[Depends(auth_user.access_from_student(current_user))]
)


@router.get(
    "/get_user_role",
    description="Получить роль пользователя",
    response_model=UserRole,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_user_role(
        user_id: int, session: AsyncSession = Depends(get_async_session)
):
    role = await DatabaseWorker(session).get_user_role(user_id)

    return {"role": role}


#
# @router.get(
#     "/get_marks",
#     description="Получить список оценок взвода",
#     response_model=list[SubjectDTO],
#     status_code=HTTPStatus.OK,
# )
# @exception_handler
# async def get_marks(session: AsyncSession = Depends(get_async_session)):
#     pass


@router.get(
    "/get_user",
    description="Получить пользователя",
    response_model=UserRead,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await DatabaseWorker(session).get_user(user_id)

    return UserRead.model_validate(user, from_attributes=True)


@router.get(
    "/get_user_by_tg",
    description="Получить пользователя по его телеграм id",
    response_model=UserRead,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_user_by_tg(
        telegram_id: int, session: AsyncSession = Depends(get_async_session)
):
    user = await DatabaseWorker(session).get_user_by_tg(telegram_id)

    return UserRead.model_validate(user, from_attributes=True)


@router.get(
    "/get_id_from_tg",
    description="Получить id пользователя по его телеграм id",
    response_model=UserID,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_id_from_tg(
        telegram_id: int, session: AsyncSession = Depends(get_async_session)
):
    user_id = await DatabaseWorker(session).get_tg_from_id(telegram_id)

    return {"id": user_id}


@router.get(
    "/get_students_list",
    description="Получить список всех студентов",
    response_model=list[Student],
    status_code=HTTPStatus.OK,
)
@exception_handler
@cache(expire=3600)
async def get_students_list(session: AsyncSession = Depends(get_async_session)):
    students = await DatabaseWorker(session).get_students_list()

    return [
        Student.model_validate(student, from_attributes=True) for student in students
    ]


@router.get(
    "/get_attendance_status_user",
    description="Получить посещаемость по студенту",
    status_code=HTTPStatus.OK,
    response_model=list[AttendDTO]
)
@exception_handler
async def get_attendance_status_user(
        user_id: int, session: AsyncSession = Depends(get_async_session)
):
    attendances = await DatabaseWorker(session).get_attendance_status_user(user_id)

    return [
        AttendDTO.model_validate(attendance, from_attributes=True) for attendance in attendances
    ]


@router.patch(
    "/set_user_attr",
    description="Установить атрибут(ы) пользователя в некоторое значение",
    status_code=HTTPStatus.NO_CONTENT,
)
@exception_handler
async def set_user_attr(
        attrs: UserSetAttr, session: AsyncSession = Depends(get_async_session)
):
    data = {
        attr: value
        for attr, value in convert_schema_to_dict(attrs.data).items()
        if value is not None
    }
    await DatabaseWorker(session).set_user_attr(attrs.id, **data)


@router.patch(
    "/set_user_mail",
    description="Установить почту пользователя в некоторое значение",
    status_code=HTTPStatus.NO_CONTENT,
)
@exception_handler
async def set_user_email(
        u_email: UserSetMail, session: AsyncSession = Depends(get_async_session)
):
    if await DatabaseWorker(session).email_is_exist(u_email.email):
        raise EmailError(
            message=f"Email {u_email.email} already exists.",
            status_code=HTTPStatus.BAD_REQUEST,
        )

    await DatabaseWorker(session).set_user_attr(u_email.id, email=u_email.email)
