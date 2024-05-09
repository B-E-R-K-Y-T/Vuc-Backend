from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from schemas.grading import UpdateGrading
from services.auth.auth import auth_user
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.database.worker import DatabaseWorker, get_database_worker

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/gradings",
    dependencies=[Depends(auth_user.access_from_professor(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.post(
    "/set_grading_theme",
    description="Создание темы урока на взвод",
    status_code=HTTPStatus.CREATED,
    response_model=list[Optional[int]]
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_grading_theme(
        platoon_number: int,
        theme_of_lesson: str,
        subj_id: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    platoon_users_id = await db_worker.get_users_id_by_platoon(platoon_number)
    res = []

    for user_id in platoon_users_id:
        grading_id: int = await db_worker.set_theme_to_subject(user_id, theme_of_lesson, subj_id)

        res.append(grading_id)

    return res


@router.patch(
    "/edit_grading",
    description="Редактирование оценки",
    status_code=HTTPStatus.OK
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_grading_theme(
        grading_id: int,
        mark: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    await db_worker.update_grading(grading_id, mark)


@router.patch(
    "/update_gradings",
    description="Массовое обновление оценок",
    status_code=HTTPStatus.CREATED
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def update_gradings(
        gradings: list[UpdateGrading],
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    for grading in gradings:
        await db_worker.update_grading(grading.id, grading.mark)


@router.get(
    "/get_gradings_by_sem",
    description="Получить оценки за семестр",
    status_code=HTTPStatus.CREATED,
    response_model=Optional[dict]
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def get_gradings_by_sem(
        semester: int,
        discipline: str,
        platoon_number: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    if semester <= 0:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    gradings = await db_worker.get_gradings(semester, discipline, platoon_number)
    res = {}

    for item in gradings:
        grading = item[1].convert_to_dict()
        theme = grading.pop("theme")
        grading["name"] = item[0]

        if not res.get(theme):
            res[theme] = [{grading.pop("id"): grading}]
        else:
            res[theme].append({grading.pop("id"): grading})

    return res
