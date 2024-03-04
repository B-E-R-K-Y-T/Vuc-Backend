import os

from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import PostgresDsn, Field

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Roles:
    admin = "Admin"
    professor = "Преподаватель"
    platoon_commander = "Командир взвода"
    squad_commander = "Командир отделения"
    student = "Студент"


class AppSettings(BaseSettings):
    APP_TITLE: str = "DefaultApp"
    DATABASE_DSN: PostgresDsn
    TEST_DATABASE_DSN: PostgresDsn
    PROJECT_HOST: str = Field("127.0.0.1", env="PROJECT_HOST")
    PROJECT_PORT: int = Field(8000, env="PROJECT_PORT")
    TOKEN_LENGTH: int = Field(25, env="TOKEN_LENGTH")
    SECRET_JWT_KEY: str
    AUTH_USER_SECRET_TOKEN: str
    DOCS_URL: str
    PASSWORD_ADMIN_PANEL: str
    LOGIN_ADMIN_PANEL: str
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


app_settings = AppSettings()
