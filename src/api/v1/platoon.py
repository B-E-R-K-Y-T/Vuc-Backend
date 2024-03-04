from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from schemas.platoon import PlatoonDTO, CountSquadDTO, PlatoonNumberDTO, PlatoonsDTO
from schemas.user import UserDTO, UserCreate, UserRead
from services.auth.auth import auth_user
from services.util import exception_handler
from services.database.worker import DatabaseWorker, get_database_worker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/platoons",
    dependencies=[Depends(auth_user.access_from_platoon_commander(current_user))],
)


@router.post(
    "/create",
    description="Создание взвода",
    response_model=PlatoonNumberDTO,
    status_code=HTTPStatus.CREATED,
)
@exception_handler
async def register(
    platoon: PlatoonDTO, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    await db_worker.create_platoon(platoon)

    return {"platoon_number": platoon.platoon_number}


@router.get(
    "/get_platoon",
    description="Получить список взвода",
    response_model=list[UserCreate],
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_platoon(
    platoon_number: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    platoon = await db_worker.get_platoon(platoon_number)

    return [UserDTO.model_validate(user, from_attributes=True) for user in platoon]


@router.get(
    "/get_platoons",
    description="Получить список взводов",
    response_model=PlatoonsDTO,
    status_code=HTTPStatus.OK,
)
@exception_handler
@cache(expire=3600)
async def get_platoons(db_worker: DatabaseWorker = Depends(get_database_worker)):
    platoons = await db_worker.get_platoons()

    data = platoons.all()
    transformed_data = {}

    for model in data:
        item = model.convert_to_dict()
        platoon_number = item["platoon_number"]
        transformed_data[platoon_number] = {
            "vus": item["vus"],
            "semester": item["semester"],
        }

    return PlatoonsDTO(data=transformed_data)


@router.get(
    "/get_platoon_commander",
    description="Получить командира взвода",
    response_model=UserRead,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_platoons(
    platoon_number: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    commander = await db_worker.get_platoon_commander(platoon_number)

    return UserRead.model_validate(commander, from_attributes=True)


@router.get(
    "/get_count_squad_in_platoon",
    description="Получить кол-во отделений во взводе",
    response_model=CountSquadDTO,
    status_code=HTTPStatus.OK,
)
@exception_handler
async def get_count_squad_in_platoon(
    platoon_number: int, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    count_squad = await db_worker.get_count_squad_in_platoon(
        platoon_number
    )

    return {"count_squad": count_squad}
