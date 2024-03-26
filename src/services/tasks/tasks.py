import requests

from config import app_settings
from services.current_weekday import get_current_day_of_the_week, Day
from .dispatcher import celery
from .types import TaskTypes
from .database import DatabaseWorker


@celery.task()
def set_attend_all_students_by_weekday():
    db_worker = DatabaseWorker()
    viewed_days = set()

    while True:
        weekday: Day = get_current_day_of_the_week()

        if len(viewed_days) == 7:
            viewed_days.clear()

        if weekday.number in viewed_days:
            continue

        users_id: list = db_worker.get_current_day_of_week_users_id(weekday.number)

        for user_id in users_id:
            db_worker.set_attend(user_id)

        viewed_days.add(weekday.number)


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
