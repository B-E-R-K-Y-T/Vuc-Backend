from http import HTTPStatus

from sqlalchemy import insert, select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from config import Roles
from exceptions import PlatoonError
from models import User, Platoon
from services.database.connector import session_init, BaseTable


class DatabaseWorker:
    @classmethod
    @session_init
    async def get_platoon(cls, platoon_number: int, session: AsyncSession):
        if not await cls.platoon_number_is_exist(platoon_number):
            raise PlatoonError(
                f"{platoon_number=} not found",
                status=HTTPStatus.NOT_FOUND
            )

        query = select(User).where(platoon_number == User.platoon_number)

        users = await session.scalars(query)
        await session.commit()

        return users

    @classmethod
    @session_init
    async def get_platoons(cls, session: AsyncSession):
        query = select(Platoon)

        platoons = await session.scalars(query)
        await session.commit()

        return platoons

    @classmethod
    @session_init
    async def get_platoon_commander(cls, platoon_number: int, session: AsyncSession) -> dict:
        query = (select(User)
                 .where(and_(User.role == Roles.platoon_commander,
                             User.platoon_number == platoon_number)
                        )
                 )

        commander = await session.scalar(query)
        await session.commit()

        return commander.convert_to_dict()

    @classmethod
    @session_init
    async def create_platoon(cls, platoon: Platoon, session: AsyncSession):
        if await cls.platoon_number_is_exist(platoon.platoon_number):
            raise PlatoonError(
                f"{platoon.platoon_number=} already exist",
                status=HTTPStatus.BAD_REQUEST
            )

        stmt = insert(Platoon).values(**dict(platoon))

        await session.execute(stmt)
        await session.commit()

    @classmethod
    @session_init
    async def get_count_squad_in_platoon(cls, platoon_number: int, session: AsyncSession) -> int:
        query = (select(func.sum(1)).
        select_from(
            select(User.squad_number).
            where(User.platoon_number == platoon_number, User.squad_number.in_([1, 2, 3])).
            group_by(User.squad_number).subquery())
        )

        count = await session.scalar(query)
        await session.commit()

        return count

    @classmethod
    async def telegram_id_is_exist(cls, telegram_id: int) -> bool:
        return await cls._check_exist_entity_column(User, {User.telegram_id.name: telegram_id})

    @classmethod
    async def platoon_number_is_exist(cls, platoon_number: int) -> bool:
        return await cls._check_exist_entity(Platoon, platoon_number)

    @classmethod
    async def platoon_commander_is_exist(cls, platoon_number: int) -> bool:
        return await cls._check_exist_entity(User, Roles.platoon_commander, platoon_number)

    @staticmethod
    @session_init
    async def _check_exist_entity(entity: BaseTable, *entity_id, session: AsyncSession) -> bool:
        ent = await session.get(entity, list[entity_id])

        if ent is not None:
            return True

        return False

    @staticmethod
    @session_init
    async def _check_exist_entity_column(entity: BaseTable, columns: dict, session: AsyncSession) -> bool:
        query = select(entity).filter_by(**columns)
        res = await session.scalar(query)

        if res is not None:
            return True

        return False
