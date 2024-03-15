from http import HTTPStatus

from fastapi import APIRouter, Depends

from services.auth.auth import auth_user
from services.util import exception_handler, convert_schema_to_dict
from schemas.professor import Semesters, AttendanceDTO, Professor
from services.database.worker import DatabaseWorker, get_database_worker

current_user = auth_user.current_user()
router = APIRouter(prefix="/professor", dependencies=[Depends(auth_user.access_from_student(current_user))])


@router.get(
    "/get_semesters",
    description="Получить список семестров",
    response_model=Semesters,
    status_code=HTTPStatus.OK
)
@exception_handler
async def get_semesters(
        user_id: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    semesters = await db_worker.get_semesters(user_id)

    return Semesters.model_validate(semesters, from_attributes=True)


@router.post(
    "/set_visit_user",
    description="Установить посещение для юзера в конкретную дату",
    status_code=HTTPStatus.NO_CONTENT,
)
@exception_handler
async def set_visit_user(
        attendance: AttendanceDTO, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    await db_worker.set_visit_user(**convert_schema_to_dict(attendance))


@router.get(
    "/get_professors_list",
    description="Получить список всех преподавателей",
    response_model=list[Professor],
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_professors_list(db_worker: DatabaseWorker = Depends(get_database_worker)):
    professors = await db_worker.get_professors_list()

    return [
        Professor.model_validate(professor, from_attributes=True)
        for professor in professors
    ]
