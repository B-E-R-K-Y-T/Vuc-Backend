from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from schemas.day import DayCreate
from services.auth.auth import auth_user
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.database.worker import DatabaseWorker, get_database_worker

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/days",
    dependencies=[Depends(auth_user.access_from_professor(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.post(
    "/set_days",
    description="Ручка для вбивания дней с днём недели в таблице Days в период от n до m",
    response_model=list[int],
    status_code=HTTPStatus.OK,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def set_days(
        request: Request,
        days: list[DayCreate],
        db_worker: DatabaseWorker = Depends(get_database_worker)
):
    days_id = []

    for day in days:
        days_id.append(
            await db_worker.set_day(
                date=day.date,
                weekday=day.weekday,
                semester=day.semester,
                holiday=day.holiday
            )
        )

    return days_id
