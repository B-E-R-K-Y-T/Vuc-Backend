from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import schemas.user
from models import User
from services.auth.auth import auth_user
from services.database.connector import get_async_session
from services.util import exception_handler
from services.database.worker import DatabaseWorker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/users",
)


# @router.post("/register",
#              description='Регистрация пользователя',
#              response_model=schemas.user.UserCreateResponse,
#              status_code=HTTPStatus.CREATED)
@exception_handler
async def register(user: schemas.user.UserDTO, session: AsyncSession = Depends(get_async_session)):
    token = await DatabaseWorker.register_user(user, session)

    return {'token': token}


@router.get("/admin-protected-route")
@exception_handler
async def admin_protected_route(user: User = Depends(auth_user.access_from_admin(current_user))):
    p = await DatabaseWorker.get_platoon(0)
    print(p.vus)

    return p


@router.get("/student-protected-route")
@exception_handler
async def student_protected_route(user: User = Depends(auth_user.access_from_student(current_user))):
    return f"Hello, {user.name}, {await DatabaseWorker.platoon_number_is_exist(236666660)}"
