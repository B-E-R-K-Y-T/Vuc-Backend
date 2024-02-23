from fastapi import FastAPI

from config import app_settings
from api.v1.user import router as user_router
from api.v1.platoon import router as platoon_router


app = FastAPI(
    title=app_settings.APP_TITLE
)

app.include_router(
    user_router,
    tags=["User"],
)
app.include_router(
    platoon_router,
    tags=["Platoon"],
)
