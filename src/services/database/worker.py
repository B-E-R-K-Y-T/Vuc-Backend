from http import HTTPStatus

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import PlatoonError
from schemas.platoon import Platoon
from models import User, Platoon
from services.database.connector import session_init


class DatabaseWorker:
    @classmethod
    @session_init
    async def telegram_id_is_exist(cls, user, session: AsyncSession) -> bool:
        query = select(User.telegram_id).where(User.telegram_id == user.telegram_id).limit(1)

        telegram_id = await session.scalar(query)

        if telegram_id is not None:
            return True

        return False

    @classmethod
    @session_init
    async def get_platoon(cls, platoon_number: int, session: AsyncSession) -> dict:
        if not await cls.platoon_is_exist(platoon_number):
            raise PlatoonError(
                f"{platoon_number=} not found",
                status=HTTPStatus.NOT_FOUND
            )

        query = select(Platoon).where(Platoon.platoon_number == platoon_number)

        platoon = await session.scalar(query)
        await session.commit()

        return platoon.as_dict()

    @staticmethod
    @session_init
    async def platoon_is_exist(platoon_number: int, session: AsyncSession) -> bool:
        query = select(Platoon).where(Platoon.platoon_number == platoon_number)

        platoon = await session.scalar(query)
        await session.commit()

        if platoon is not None:
            return True

        return False

    @classmethod
    @session_init
    async def create_platoon(cls, platoon: Platoon, session: AsyncSession):
        if await cls.platoon_is_exist(platoon.platoon_number):
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
