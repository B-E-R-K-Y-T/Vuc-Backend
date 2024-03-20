from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from schemas.attend import ConfirmationAttend
from services.auth.auth import auth_user
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.database.worker import DatabaseWorker, get_database_worker

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/attends",
    dependencies=[Depends(auth_user.access_from_squad_commander(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.patch(
    "/confirmation_attend_user",
    description="Подтверждение посещения",
    status_code=HTTPStatus.CREATED
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
@collector.cache()
async def set_attend_user(
    attend: ConfirmationAttend,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    await db_worker.confirmation_attend_user(attend)
