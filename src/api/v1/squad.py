from http import HTTPStatus

from fastapi import APIRouter, Depends

from services.auth.auth import auth_user
from services.util import exception_handler
from schemas.user import UserDTO
from services.database.worker import DatabaseWorker, get_database_worker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/squad",
    dependencies=[Depends(auth_user.access_from_squad_commander(current_user))],
)


@router.get(
    "/get_students_by_squad",
    description="Получить студентов в отделении",
    response_model=list[UserDTO],
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_subject_by_semester(
        platoon_number: int,
        squad_number: int,
        db_worker: DatabaseWorker = Depends(get_database_worker),
):
    users = await db_worker.get_users_by_squad(platoon_number, squad_number)

    return [UserDTO.model_validate(user, from_attributes=True) for user in users]
