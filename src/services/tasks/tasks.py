from celery import Celery

from config import app_settings

celery = Celery('tasks', broker=f'redis://{app_settings.REDIS_HOST}:{app_settings.REDIS_PORT}')
