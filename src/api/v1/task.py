from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import app_settings
from services.auth.auth import auth_user
from services.event_system.event_bus import EventBus
from services.event_system.handlers import send_message_user_handler
from services.event_system.types import TypeEvent

limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/task",
    dependencies=[Depends(auth_user.access_from_professor(current_user))],
)
event_bus = EventBus()


@router.post(
    "/send_message_user",
    status_code=HTTPStatus.OK,
)
@limiter.limit(app_settings.MAX_REQUESTS_TO_ENDPOINT)
async def send_message_user(
        telegram_id: int,
        message: str,
        request: Request,
):
    print(telegram_id, message)
    event_bus.subscribe_event(
        event=TypeEvent.MESSAGE_TO_SPECIFIC_USER,
        func=send_message_user_handler,
        kwargs={"telegram_id": telegram_id, "message": message}
    )
