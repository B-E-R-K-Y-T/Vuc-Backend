from http import HTTPStatus
from typing import Dict

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from services.auth.auth import auth_user
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.util import convert_schema_to_dict, result_collection_builder
from schemas.professor import Semesters, AttendanceDTO, Professor
from services.database.worker import DatabaseWorker, get_database_worker

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/professor",
    dependencies=[Depends(auth_user.access_from_student(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.get(
    "/get_semesters",
    description="Получить список семестров",
    response_model=Semesters,
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


@router.post(
    "/set_visit_user",
    description="Установить посещение для юзера в конкретную дату",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(auth_user.access_from_squad_commander(current_user))],
    response_model=int,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def set_visit_user(
        attendance: AttendanceDTO,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    return await db_worker.set_visit_user(**convert_schema_to_dict(attendance))


@router.get(
    "/get_professors_list",
    description="Получить всех преподавателей",
    response_model=Dict[int | str, Professor],
    status_code=HTTPStatus.OK,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def get_professors_list(
        request: Request, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    professors = await db_worker.get_professors_list()

    return await result_collection_builder(professors, schema=Professor)
