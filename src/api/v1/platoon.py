from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import platoon as platoon_schema
from services.database.connector import get_async_session
from services.util import exception_handler
from services.database.worker import DatabaseWorker

router = APIRouter(
    prefix="/platoons"
)


@router.post("/create",
             description='Создание взвода',
             response_model=platoon_schema.PlatoonNumber,
             status_code=HTTPStatus.CREATED)
async def register(platoon: platoon_schema.Platoon, session: AsyncSession = Depends(get_async_session)):
    await DatabaseWorker.create_platoon(platoon, session)

    return {'platoon_number': platoon.platoon_number}


"""
@app.route(EndPoint.GET_COUNT_PLATOON_SQUAD)
def get_count_platoon_squad():
    platoon_number = request.args.get('platoon_number')
    return db.get_count_squad_in_platoon(int(platoon_number))


@app.route(EndPoint.GET_PLATOON_COMMANDER)
def get_platoon_commander():
    platoon_number = request.args.get('platoon_number')
    return db.get_platoon_commander(int(platoon_number))

"""


@router.get("/get_platoon",
            description='Получить взвод',
            response_model=platoon_schema.Platoon,
            status_code=HTTPStatus.OK)
async def get_platoon(platoon_number: int, session: AsyncSession = Depends(get_async_session)):
    platoon = await DatabaseWorker.get_platoon(platoon_number, session)

    return platoon


@router.get("/get_count_squad_in_platoon",
            description='Получить кол-во отделений во взводе',
            response_model=platoon_schema.CountSquad,
            status_code=HTTPStatus.OK)
async def get_count_squad_in_platoon(platoon_number: int, session: AsyncSession = Depends(get_async_session)):
    count = await DatabaseWorker.get_count_squad_in_platoon(platoon_number, session)

    return {'count': count}
