import requests

from config import app_settings
from services.current_weekday import get_current_day_of_the_week, Day
from .dispatcher import celery
from .types import TaskTypes, StatusTask
from .database import DatabaseWorker


def _check_view_day_of_week(viewed_days: set):
    def checker(day_of_week: Day):
        if len(viewed_days) == 7:
            viewed_days.clear()

        if day_of_week.number in viewed_days:
            return True

        viewed_days.add(day_of_week.number)

        return False

    return checker


@celery.task()
def set_attend_all_students_by_weekday():
    db_worker = DatabaseWorker()
    viewed_days = set()
    check_day_viewed = _check_view_day_of_week(viewed_days)

    while True:
        weekday: Day = get_current_day_of_the_week()

        if check_day_viewed(weekday):
            continue

        users_id: list = db_worker.get_day_of_week_users_id(weekday.number)

        for user_id in users_id:
            db_worker.set_attend(user_id)


@celery.task()
def answer_platoon_about_attend():
    db_worker = DatabaseWorker()
    viewed_days = set()
    check_day_viewed = _check_view_day_of_week(viewed_days)

    while True:
        weekday: Day = get_current_day_of_the_week()

        if check_day_viewed(weekday):
            continue

        users_id: list = db_worker.get_day_of_week_users_id(weekday.number + 1 if 1 <= weekday.number < 7 else 1)

        res = []

        for user_id in users_id:
            res.append(
                requests.post(
                    f"{app_settings.BOT_ADDRESS}/tasks",
                    json={
                        "type": TaskTypes.ANSWER_ATTEND,
                        "auth_token": app_settings.AUTH_BOT_TOKEN,
                        "telegram_id": db_worker.get_telegram_id(user_id),
                        "message": "Будете ли Вы на следующем занятии?"
                    }
                )
            )

        return [item.json() if item.status_code < 400 else {"status_task": StatusTask.ERROR} for item in res]


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
