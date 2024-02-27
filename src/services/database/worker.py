from http import HTTPStatus

from sqlalchemy import insert, select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from config import Roles
from exceptions import PlatoonError
from models import User, Platoon
from schemas.platoon import PlatoonDTO
from services.database.connector import BaseTable


class DatabaseWorker:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_platoon(self, platoon_number: int):
        query = select(User).where(platoon_number == User.platoon_number)

        users = await self.session.scalars(query)
        await self.session.commit()

        return users

    async def get_platoons(self):
        query = select(Platoon)

        platoons = await self.session.scalars(query)
        await self.session.commit()

        return platoons

    async def get_platoon_commander(self, platoon_number: int) -> dict:
        query = (select(User)
                 .where(and_(User.role == Roles.platoon_commander,
                             User.platoon_number == platoon_number)
                        )
                 )

        commander = await self.session.scalar(query)
        await self.session.commit()

        if commander is None:
            raise PlatoonError(
                message=f'Командир во взводе "{platoon_number}" не найден',
                status_code=HTTPStatus.NOT_FOUND
            )

        return commander.convert_to_dict()

    async def create_platoon(self, platoon: PlatoonDTO):
        if await self.platoon_number_is_exist(platoon.platoon_number):
            raise PlatoonError(
                f"{platoon.platoon_number=} already exist",
                status_code=HTTPStatus.BAD_REQUEST
            )

        stmt = insert(Platoon).values(**dict(platoon))

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_count_squad_in_platoon(self, platoon_number: int) -> int:
        query = (
            select(func.sum(1)).
            select_from(
                select(User.squad_number).
                where(User.platoon_number == platoon_number, User.squad_number.in_([1, 2, 3])).
                group_by(User.squad_number).subquery())
        )

        count = await self.session.scalar(query)
        await self.session.commit()

        return count

    async def telegram_id_is_exist(self, telegram_id: int) -> bool:
        return await self._check_exist_entity_column(User, {User.telegram_id.name: telegram_id})

    async def platoon_number_is_exist(self, platoon_number: int) -> bool:
        return await self._check_exist_entity(Platoon, platoon_number)

    async def platoon_commander_is_exist(self, platoon_number: int) -> bool:
        query = (
            select(User).
            where(
                and_(
                    User.platoon_number == platoon_number,
                    User.role == Roles.platoon_commander
                )
            )
        )

        commander = await self.session.scalar(query)

        if commander is not None:
            return True

        return False

    async def _check_exist_entity(self, entity: BaseTable, entity_id) -> bool:
        ent = await self.session.get(entity, entity_id)

        if ent is not None:
            return True

        return False

    async def _check_exist_entity_column(self, entity: BaseTable, columns: dict) -> bool:
        query = select(entity).filter_by(**columns)
        res = await self.session.scalar(query)

        if res is not None:
            return True

        return False
