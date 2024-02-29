from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.auth import auth_user
from services.database.connector import get_async_session
from services.util import exception_handler
from schemas.professor import SubjectDTO
from services.database.worker import DatabaseWorker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/professor"
)


@router.get("/get_subjects",
            description='Получить список дисциплин взвода',
            response_model=list[SubjectDTO],
            status_code=HTTPStatus.OK)
@exception_handler
async def get_subjects(platoon_number: int, semester: int, session: AsyncSession = Depends(get_async_session)):
    subjects = await DatabaseWorker(session).get_subjects(platoon_number, semester)

    return [SubjectDTO.model_validate(subject, from_attributes=True) for subject in subjects]


@router.get("/get_marks",
            description='Получить список дисциплин взвода',
            response_model=list[SubjectDTO],
            status_code=HTTPStatus.OK)
@exception_handler
async def get_marks(session: AsyncSession = Depends(get_async_session)):
    pass
