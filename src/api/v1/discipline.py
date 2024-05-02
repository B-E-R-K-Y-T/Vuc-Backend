from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from schemas.discipline import DisciplineCreate
from services.auth.auth import auth_user
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.database.worker import DatabaseWorker, get_database_worker

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/disciplines",
    dependencies=[Depends(auth_user.access_from_professor(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.post(
    "/set_discipline",
    description="Выдать поощрение или взыскание",
    response_model=int,
    status_code=HTTPStatus.CREATED,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_discipline(
        request: Request,
        discipline: DisciplineCreate,
        db_worker: DatabaseWorker = Depends(get_database_worker)
):
    return await db_worker.set_discipline(
        discipline.user_id,
        discipline.type.value,
        discipline.comment,
        discipline.date
    )


@router.get(
    "/get_discipline",
    description="Получить поощрение или взыскание по студенту за семестр",
    response_model=list[dict],
    status_code=HTTPStatus.OK,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def get_discipline(
        user_id: int,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker)
):
    discipline_sem = await db_worker.get_discipline(user_id)
    res = []

    for discipline in discipline_sem:
        res.append(discipline.convert_to_dict())

    return res
