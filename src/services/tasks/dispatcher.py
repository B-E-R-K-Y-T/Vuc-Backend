import redis
from celery import Celery
from celery.result import AsyncResult

from config import app_settings

celery = Celery(
    "tasks",
    broker=f"redis://{app_settings.REDIS_HOST}:{app_settings.REDIS_PORT}",
    backend=f"redis://{app_settings.REDIS_HOST}:{app_settings.REDIS_PORT}"
)
celery.conf.task_serializer = 'json'
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)

redis_client = redis.Redis(host=app_settings.REDIS_HOST, port=app_settings.REDIS_PORT)


def get_task_status(task_id):
    result = AsyncResult(task_id, app=celery)

    return result.state


def get_task_result(task_id):
    result = AsyncResult(task_id, app=celery)

    if result.successful():
        return result.get()

    return {"task_id": task_id, "state": result.state, "result": "Not ready"}
