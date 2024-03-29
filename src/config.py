import os

from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import PostgresDsn, Field

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    APP_TITLE: str = "DefaultApp"
    DATABASE_DSN: PostgresDsn
    PROJECT_HOST: str = Field('127.0.0.1', env='PROJECT_HOST')
    PROJECT_PORT: int = Field(8000, env='PROJECT_PORT')

    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}\\.env')


app_settings = AppSettings()

