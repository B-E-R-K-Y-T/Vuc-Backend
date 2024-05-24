from http import HTTPStatus
from typing import Dict

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from exceptions import UserNotFound
from schemas.user import UserDTO
from services.auth.auth import auth_user
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.util import convert_schema_to_dict, result_collection_builder
from schemas.professor import Semesters, AttendanceDTO, Professor, AttendancePlatoon, AttendanceReplace
from services.database.worker import DatabaseWorker, get_database_worker

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/professor",
    dependencies=[Depends(auth_user.access_from_professor(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.get(
    "/get_semesters",
    description="Получить список семестров",
    response_model=Semesters,
    dependencies=[Depends(auth_user.access_from_student(current_user))],
    status_code=HTTPStatus.OK,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def get_semesters(
        user_id: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    semesters = await db_worker.get_semesters(user_id)

    return Semesters.model_validate(semesters, from_attributes=True)


@router.get(
    "/get_semesters_platoon",
    description="Получить список семестров взвода",
    response_model=Semesters,
    dependencies=[Depends(auth_user.access_from_student(current_user))],
    status_code=HTTPStatus.OK,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def get_semesters(
        platoon_number: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    user_id = (await db_worker.get_platoon_commander(platoon_number))["id"]
    semesters = await db_worker.get_semesters(user_id)

    return Semesters.model_validate(semesters, from_attributes=True)


@router.post(
    "/set_visit_user",
    description="Создать посещение для юзера в конкретную дату",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(auth_user.access_from_student(current_user))],
    response_model=int,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_visit_user(
        attendance: AttendanceDTO,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    return await db_worker.set_visit_user(**convert_schema_to_dict(attendance))


@router.post(
    "/set_visit_user_confirmed",
    description="Создать посещение для юзера в конкретную дату",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(auth_user.access_from_professor(current_user))],
    response_model=int,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_visit_user_confirmed(
        attendance: AttendanceDTO,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    return await db_worker.set_visit_user(**convert_schema_to_dict(attendance), confirmed=True)


@router.patch(
    "/set_visit_user",
    description="Заменить посещение для юзера в конкретную дату",
    status_code=HTTPStatus.OK,
    dependencies=[Depends(auth_user.access_from_student(current_user))]
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_visit_user(
        attendance: AttendanceReplace,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    await db_worker.replace_visit(**convert_schema_to_dict(attendance))


@router.post(
    "/set_visit_users",
    description="Установить посещение для нескольких пользователей в конкретную дату",
    status_code=HTTPStatus.CREATED,
    response_model=list[int],
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_visit_users(
        attendances: list[AttendanceDTO],
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    for attendance in attendances:
        if not await db_worker.user_is_exist(attendance.user_id):
            raise UserNotFound(
                message=f"User {attendance.user_id} not found",
                status_code=HTTPStatus.NOT_FOUND,
            )

    res = []

    # TODO: Сделать один insert на список, а не создавать по запросу на элемент списка
    for attendance in attendances:
        res.append(await db_worker.set_visit_user(**convert_schema_to_dict(attendance)))

    return res


@router.post(
    "/set_visit_platoon",
    description="Установить посещение для взвода в конкретную дату",
    status_code=HTTPStatus.CREATED,
    response_model=list[int],
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_visit_platoon(
        attendance: AttendancePlatoon,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    res = []

    platoon = await db_worker.get_platoon(attendance.platoon_number)
    students = await result_collection_builder(platoon, schema=UserDTO)
    attendance_dict = convert_schema_to_dict(attendance)
    semester = attendance.semester if attendance.semester else None

    # TODO: Сделать один insert на список, а не создавать по запросу на элемент списка
    for student_id in students.keys():
        res.append(
            await db_worker.set_visit_user(
                date_v=attendance_dict["date_v"],
                visiting=attendance_dict["visiting"],
                user_id=student_id,
                semester=semester,
                confirmed=True
            )
        )

    return res


@router.get(
    "/get_professors_list",
    description="Получить всех преподавателей",
    response_model=Dict[int | str, Professor],
    dependencies=[Depends(auth_user.access_from_student(current_user))],
    status_code=HTTPStatus.OK,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def get_professors_list(
        request: Request, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    professors = await db_worker.get_professors_list()

    return await result_collection_builder(professors, schema=Professor)
