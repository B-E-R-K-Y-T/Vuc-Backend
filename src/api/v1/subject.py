import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from exceptions import SemesterError
from services.auth.auth import auth_user
from schemas.professor import SubjectDTO, Gradings
from services.database.worker import DatabaseWorker, get_database_worker


limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/subject",
    dependencies=[Depends(auth_user.access_from_student(current_user))],
)


@router.get(
    "/get_subject_by_semester",
    description="Получить список дисциплин взвода",
    response_model=list[SubjectDTO],
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_subject_by_semester(
    platoon_number: int,
    semester: int,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    subjects = await db_worker.get_subjects(platoon_number, semester)

    return [
        SubjectDTO.model_validate(subject, from_attributes=True) for subject in subjects
    ]


@router.get(
    "/get_subject_by_now_semester",
    description="Получить список дисциплин взвода за текущий семестр",
    response_model=list[SubjectDTO],
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_subject_by_now_semester(
    platoon_number: int,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    if 9 <= datetime.date.today().month <= 12:
        semester = 1
    elif 1 <= datetime.date.today().month <= 6:
        semester = 2
    else:
        raise SemesterError(
            message="Сейчас не идет учеба", status_code=HTTPStatus.BAD_REQUEST
        )

    subjects = await db_worker.get_subjects(platoon_number, semester)

    return [
        SubjectDTO.model_validate(subject, from_attributes=True) for subject in subjects
    ]


@router.get(
    "/get_gradings_by_student",
    description="Получить список оценок за конкретный предмет у конкретного студента",
    response_model=list[Gradings],
    status_code=HTTPStatus.OK,
    dependencies=[Depends(auth_user.access_from_student(current_user))],
)
@limiter.limit("5/minute")
async def get_gradings_by_student(
    user_id: int,
    subject_id: int,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    gradings = await db_worker.get_gradings_by_student(user_id, subject_id)

    return [
        Gradings.model_validate(grading, from_attributes=True) for grading in gradings
    ]
