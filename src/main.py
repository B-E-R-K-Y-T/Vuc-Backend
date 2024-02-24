import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from config import app_settings
from api.v1.user import router as user_router
from api.v1.platoon import router as platoon_router
from schemas.user import UserRead, UserCreate
from services.auth.auth import auth_backend, auth_fastapi_users

app = FastAPI(
    title=app_settings.APP_TITLE,
    # Адрес документации в красивом интерфейсе
    docs_url=app_settings.DOCS_URL,
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(
    user_router,
    tags=["User"],
)
app.include_router(
    platoon_router,
    tags=["Platoon"],
)
app.include_router(
    auth_fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    auth_fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 127.0.0.1 --port 8080`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host=app_settings.PROJECT_HOST,
        port=app_settings.PROJECT_PORT,
        reload=True,
    )
