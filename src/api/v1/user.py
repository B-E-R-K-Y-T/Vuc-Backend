from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserRole
from services.auth.auth import auth_user
from services.database.connector import get_async_session
from services.util import exception_handler
from services.database.worker import DatabaseWorker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/users",
)


@router.get("/get_user_role",
            description='Получить роль пользователя',
            response_model=UserRole,
            status_code=HTTPStatus.OK)
@exception_handler
async def get_user_role(user_id: int, session: AsyncSession = Depends(get_async_session)):
    commander = await DatabaseWorker(session).get_platoon_commander(user_id)

    return UserRole.model_validate(commander, from_attributes=True)
