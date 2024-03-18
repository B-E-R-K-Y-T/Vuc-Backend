from http import HTTPStatus
from typing import Dict

from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from schemas.platoon import PlatoonDTO, PlatoonNumberDTO, PlatoonDataDTO
from schemas.user import UserDTO, UserRead
from services.auth.auth import auth_user
from services.cache.collector import CacheCollector
from services.cache.containers import RedisContainer
from services.database.worker import DatabaseWorker, get_database_worker


limiter = Limiter(key_func=get_remote_address)
current_user = auth_user.current_user()
router = APIRouter(
    prefix="/platoons",
    dependencies=[Depends(auth_user.access_from_platoon_commander(current_user))],
)
collector = CacheCollector(container=RedisContainer())


@router.post(
    "/create",
    description="Создание взвода",
    response_model=PlatoonNumberDTO,
    status_code=HTTPStatus.CREATED,
)
@limiter.limit("5/minute")
async def register(
    platoon: PlatoonDTO,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    await db_worker.create_platoon(platoon)

    return {"platoon_number": platoon.platoon_number}


@router.get(
    "/get_platoon",
    description="Получить список взвода",
    response_model=list[UserDTO],
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_platoon(
    platoon_number: int,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    platoon = await db_worker.get_platoon(platoon_number)

    return [UserDTO.model_validate(user, from_attributes=True) for user in platoon]


@router.get(
    "/get_platoons",
    description="Получить список взводов",
    response_model=Dict[int | str, PlatoonDataDTO | int],
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_platoons(
    request: Request, db_worker: DatabaseWorker = Depends(get_database_worker)
):
    platoons = await db_worker.get_platoons()

    data = platoons.all()
    transformed_platoons = {"count": len(data)}

    for model in data:
        item = model[0].convert_to_dict()
        platoon_number = item["platoon_number"]
        transformed_platoons[platoon_number] = PlatoonDataDTO.model_validate(
            {
                "commander": model[1],
                "vus": item["vus"],
                "semester": item["semester"],
            },
            from_attributes=True,
        )

    return transformed_platoons


@router.get(
    "/get_platoon_commander",
    description="Получить командира взвода",
    response_model=UserRead,
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_platoon_commander(
    platoon_number: int,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    commander = await db_worker.get_platoon_commander(platoon_number)

    return UserRead.model_validate(commander, from_attributes=True)


@router.get(
    "/get_count_squad_in_platoon",
    description="Получить кол-во отделений во взводе",
    response_model=int,
    status_code=HTTPStatus.OK,
)
@limiter.limit("5/minute")
async def get_count_squad_in_platoon(
    platoon_number: int,
    request: Request,
    db_worker: DatabaseWorker = Depends(get_database_worker),
):
    return await db_worker.get_count_squad_in_platoon(platoon_number)
