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
    docs_url='/api/openapi',
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
