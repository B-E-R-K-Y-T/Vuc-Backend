import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware

from config import app_settings
from schemas.user import UserRead, UserCreate
from services.admin_panel.panel import init_admin_panel
from services.auth.auth import auth_backend, auth_user
from exceptions import MainVucException
from services.database.connector import engine
from api.v1.user import router as user_router
from api.v1.professor import router as professor_router
from api.v1.platoon import router as platoon_router
from api.v1.subject import router as subject_router

app = FastAPI(
    title=app_settings.APP_TITLE,
    # Адрес документации в Swagger интерфейсе
    docs_url=app_settings.DOCS_URL,
    # Адрес документации в формате OpenAPI
    openapi_url="/api/openapi.json",
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
    professor_router,
    tags=["Professor"],
)
app.include_router(
    subject_router,
    tags=["Subject"],
)
app.include_router(
    auth_user.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    auth_user.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

origins = app_settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup_event():
    init_admin_panel(app, engine)

    redis = aioredis.from_url(
        f"redis://{app_settings.REDIS_HOST}:{app_settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.exception_handler(MainVucException)
async def exception_handler(request: Request, exc: MainVucException):
    return ORJSONResponse(
        status_code=exc.status_code,
        content=f"Detail: {str(exc)}, JSON: {request.json()}",
    )


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 127.0.0.1 --port 8080 --reload`
    # но чтобы не терять возможность использовать дебагер,
    # запусти uvicorn сервер через python
    uvicorn.run(
        "main:app",
        host=app_settings.PROJECT_HOST,
        port=app_settings.PROJECT_PORT,
        reload=True,
    )
