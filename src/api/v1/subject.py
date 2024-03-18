import datetime
from http import HTTPStatus
from typing import Dict

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from exceptions import SemesterError
from services.auth.auth import auth_user
from schemas.professor import SubjectDTO, Gradings
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.database.worker import DatabaseWorker, get_database_worker
from services.util import result_collection_builder

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/subject",
    dependencies=[Depends(auth_user.access_from_student(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.get(
    "/get_subject_by_semester",
    description="Получить список дисциплин взвода",
    response_model=Dict[str | int, SubjectDTO],
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_subject_by_semester(
        platoon_number: int,
        semester: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    subjects = await db_worker.get_subjects(platoon_number, semester)

    return await result_collection_builder(subjects, schema=SubjectDTO)


@router.get(
    "/get_subject_by_now_semester",
    description="Получить список дисциплин взвода за текущий семестр",
    response_model=Dict[str | int, SubjectDTO],
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_subject_by_now_semester(
        platoon_number: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    if 9 <= datetime.date.today().month <= 12:
        semester = 1
    elif 1 <= datetime.date.today().month <= 6:
        semester = 2
    else:
        raise SemesterError(
            message="Сейчас не идет учеба", status_code=HTTPStatus.BAD_REQUEST
        )

    subjects = await db_worker.get_subjects(platoon_number, semester)

    return await result_collection_builder(subjects, schema=SubjectDTO)


@router.get(
    "/get_gradings_by_student",
    description="Получить список оценок за конкретный предмет у конкретного студента",
    response_model=Dict[str | int, Gradings],
    status_code=HTTPStatus.OK,
    dependencies=[Depends(auth_user.access_from_student(current_user))],
)
@limiter.limit("5/minute")
async def get_gradings_by_student(
        user_id: int,
        subject_id: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    gradings = await db_worker.get_gradings_by_student(user_id, subject_id)

    return await result_collection_builder(gradings, schema=Gradings)
