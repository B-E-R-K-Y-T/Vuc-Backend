from http import HTTPStatus

from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends

from exceptions import EmailError
from schemas.attend import AttendDTO
from schemas.grading import UserMark
from schemas.user import (
    UserRole,
    UserRead,
    UserSetAttr,
    UserSetMail,
    UserID,
    Student,
    UserDTO,
)
from services.auth.auth import auth_user
from services.util import exception_handler, convert_schema_to_dict
from services.database.worker import DatabaseWorker, get_database_worker

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
        user_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    role = await db_worker.get_user_role(user_id)

    return {"role": role}


@router.get(
    "/get_marks",
    description="Получить список оценок студента",
    response_model=list[UserMark],
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_marks(user_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)):
    marks = await db_worker.get_marks(user_id)

    return [UserMark.model_validate(mark, from_attributes=True) for mark in marks]


@router.get(
    "/get_marks_by_semester",
    description="Получить список оценок студента по семестру",
    response_model=list[UserMark],
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_marks(user_id: int, semester: int, db_worker: DatabaseWorker = Depends(get_database_worker)):
    marks = await db_worker.get_marks_by_semester(user_id, semester)

    return [UserMark.model_validate(mark, from_attributes=True) for mark in marks]


@router.get(
    "/get_user",
    description="Получить пользователя",
    response_model=UserRead,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_user(user_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)):
    user = await db_worker.get_user(user_id)

    return UserRead.model_validate(user, from_attributes=True)


@router.get(
    "/get_user_by_tg",
    description="Получить пользователя по его телеграм id",
    response_model=UserRead,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_user_by_tg(
        telegram_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    user = await db_worker.get_user_by_tg(telegram_id)

    return UserRead.model_validate(user, from_attributes=True)


@router.get(
    "/get_id_from_tg",
    description="Получить id пользователя по его телеграм id",
    response_model=UserID,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_id_from_tg(
        telegram_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    user_id = await db_worker.get_id_from_tg(telegram_id)

    return {"id": user_id}


@router.get(
    "/get_id_from_email",
    description="Получить id пользователя по его email",
    response_model=UserID,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_id_from_email(
        email: str, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    user_id = await db_worker.get_id_from_email(email)

    return {"id": user_id}


@router.get(
    "/get_students_list",
    description="Получить список всех студентов",
    response_model=list[Student],
    status_code=HTTPStatus.OK,
)
@exception_handler
# @cache(expire=300)
async def get_students_list(db_worker: DatabaseWorker = Depends(get_database_worker)):
    students = await db_worker.get_students_list()

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
        user_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    attendances = await db_worker.get_attendance_status_user(user_id)

    return [
        AttendDTO.model_validate(attendance, from_attributes=True) for attendance in attendances
    ]


@router.get(
    "/get_self",
    description="Получить информацию по студенту",
    status_code=HTTPStatus.OK,
    response_model=UserDTO
)
@exception_handler
async def get_self(
        user_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    user_self = await db_worker.get_user(user_id)

    return UserDTO.model_validate(user_self, from_attributes=True)


@router.patch(
    "/set_user_attr",
    description="Установить атрибут(ы) пользователя в некоторое значение",
    status_code=HTTPStatus.NO_CONTENT,
)
@exception_handler
async def set_user_attr(
        attrs: UserSetAttr, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    data = {
        attr: value
        for attr, value in convert_schema_to_dict(attrs.data).items()
        if value is not None
    }
    await db_worker.set_user_attr(attrs.id, **data)


@router.patch(
    "/set_user_mail",
    description="Установить почту пользователя в некоторое значение",
    status_code=HTTPStatus.NO_CONTENT,
)
@exception_handler
async def set_user_email(
        u_email: UserSetMail, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    if await db_worker.email_is_exist(u_email.email):
        raise EmailError(
            message=f"Email {u_email.email} already exists.",
            status_code=HTTPStatus.BAD_REQUEST,
        )

    await db_worker.set_user_attr(u_email.id, email=u_email.email)
