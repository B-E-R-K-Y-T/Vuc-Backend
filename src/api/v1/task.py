from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from services.auth.auth import auth_user
from services.database.worker import DatabaseWorker, get_database_worker
from services.tasks.dispatcher import get_task_status, get_task_result
from services.tasks.tasks import send_user_message, send_message_platoon

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/task",
    dependencies=[Depends(auth_user.access_from_professor(current_user))],
)


@router.get(
    "/get_status_task",
    status_code=HTTPStatus.OK,
    response_model=str
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def get_status_task(
        task_id: str,
        request: Request,
):
    return get_task_status(task_id)


@router.get(
    "/get_result_task",
    status_code=HTTPStatus.OK,
    response_model=dict
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def get_result_task(
        task_id: str,
        request: Request,
):
    return get_task_result(task_id)


@router.post(
    "/send_message_user",
    status_code=HTTPStatus.CREATED,
    response_model=dict
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def send_message_user(
        telegram_id: int,
        message: str,
        request: Request,
):
    result = send_user_message.delay(telegram_id, message)

    return {"task_id": result.task_id}


@router.post(
    "/send_message_platoon",
    status_code=HTTPStatus.CREATED,
    response_model=dict
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def send_platoon_message(
        platoon_number: int,
        message: str,
        request: Request,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    users_tg = await db_worker.get_users_telegram_id_by_platoon(platoon_number)
    result = send_message_platoon.delay(list(users_tg), message)

    return {"task_id": result.task_id}
