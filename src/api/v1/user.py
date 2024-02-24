from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import schemas.user
from models import User
from services.auth.auth import auth_fastapi_users
from services.database.connector import get_async_session
from services.util import exception_handler
from services.database.worker import DatabaseWorker

router = APIRouter(
    prefix="/users"
)
current_user = auth_fastapi_users.current_user()


# @router.post("/register",
#              description='Регистрация пользователя',
#              response_model=schemas.user.UserCreateResponse,
#              status_code=HTTPStatus.CREATED)
@exception_handler
async def register(user: schemas.user.UserCreate, session: AsyncSession = Depends(get_async_session)):
    token = await DatabaseWorker.register_user(user, session)

    return {'token': token}


@router.get("/admin-protected-route")
@exception_handler
def admin_protected_route(user: User = Depends(auth_fastapi_users.access_from_admin(current_user))):
    return f"Hello, {user.name}"


@router.get("/student-protected-route")
@exception_handler
def admin_protected_route(user: User = Depends(auth_fastapi_users.access_from_student(current_user))):
    return f"Hello, {user.name}"
