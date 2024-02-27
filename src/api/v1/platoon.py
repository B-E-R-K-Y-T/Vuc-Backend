from http import HTTPStatus

from fastapi import APIRouter, Depends

from schemas.platoon import PlatoonDTO, CountSquadDTO, PlatoonNumberDTO
from schemas.user import UserDTO, UserCreateDTO, UserReadDTO
from services.auth.auth import auth_user
from services.util import exception_handler
from services.database.worker import DatabaseWorker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/platoons",
    dependencies=[Depends(auth_user.access_from_platoon_commander(current_user))]
)


@router.post("/create",
             description='Создание взвода',
             response_model=PlatoonNumberDTO,
             status_code=HTTPStatus.CREATED)
@exception_handler
async def register(platoon: PlatoonDTO):
    await DatabaseWorker.create_platoon(platoon)

    return {'platoon_number': platoon.platoon_number}


"""

@app.route(EndPoint.GET_COUNT_PLATOON_SQUAD)
def get_count_platoon_squad():
    platoon_number = request.args.get('platoon_number')
    return db.get_count_squad_in_platoon(int(platoon_number))

"""


@router.get("/get_platoon",
            description='Получить список взвода',
            response_model=list[UserCreateDTO],
            status_code=HTTPStatus.OK)
@exception_handler
async def get_platoon(platoon_number: int):
    platoon = await DatabaseWorker.get_platoon(platoon_number)

    return [UserDTO.model_validate(user, from_attributes=True) for user in platoon]


@router.get("/get_platoons",
            description='Получить список взводов',
            response_model=list[PlatoonDTO],
            status_code=HTTPStatus.OK)
@exception_handler
async def get_platoons():
    platoons = await DatabaseWorker.get_platoons()

    return [PlatoonDTO.model_validate(platoon, from_attributes=True) for platoon in platoons]


@router.get("/get_platoon_commander",
            description='Получить командира взвода',
            response_model=UserReadDTO,
            status_code=HTTPStatus.OK)
@exception_handler
async def get_platoons(platoon_number: int):
    commander = await DatabaseWorker.get_platoon_commander(platoon_number)

    return UserReadDTO.model_validate(commander, from_attributes=True)


@router.get("/get_count_squad_in_platoon",
            description='Получить кол-во отделений во взводе',
            response_model=CountSquadDTO,
            status_code=HTTPStatus.OK)
@exception_handler
async def get_count_squad_in_platoon(platoon_number: int):
    count_squad = await DatabaseWorker.get_count_squad_in_platoon(platoon_number)

    return {'count_squad': count_squad}
