import requests

from config import app_settings
from .dispatcher import celery
from .types import TaskTypes


@celery.task
def send_user_message(telegram_id: int, message: str):
    res = requests.post(
        f"{app_settings.BOT_ADDRESS}/tasks",
        json={
            "type": TaskTypes.SEND_USER_MESSAGE,
            "auth_token": app_settings.AUTH_BOT_TOKEN,
            "telegram_id": telegram_id,
            "message": message
        }
    )

    return res.json()


@celery.task
def send_message_platoon(users_tg: list, message: str):
    res = requests.post(
        f"{app_settings.BOT_ADDRESS}/tasks",
        json={
            "type": TaskTypes.SEND_PLATOON_MESSAGE,
            "auth_token": app_settings.AUTH_BOT_TOKEN,
            "users_tg": users_tg,
            "message": message
        }
    )

    return res.json()
