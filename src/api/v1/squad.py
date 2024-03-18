from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from services.auth.auth import auth_user
from schemas.user import UserDTO
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.database.worker import DatabaseWorker, get_database_worker


limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/squad",
    dependencies=[Depends(auth_user.access_from_squad_commander(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.get(
    "/get_students_by_squad",
    description="Получить студентов в отделении",
    response_model=list[UserDTO],
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_subject_by_semester(
    platoon_number: int,
    squad_number: int,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    users = await db_worker.get_users_by_squad(platoon_number, squad_number)

    return [UserDTO.model_validate(user, from_attributes=True) for user in users]
