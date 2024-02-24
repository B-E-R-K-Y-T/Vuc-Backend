from http import HTTPStatus

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate
from schemas.platoon import Platoon
from models import User, Platoon
from services.util import TokenWorker
from exceptions import TelegramIDError


class DatabaseWorker:
    @classmethod
    async def register_user(cls, user: UserCreate, session: AsyncSession) -> str:
        query = select(User.telegram_id).where(User.telegram_id == user.telegram_id)

        telegram_id = await session.scalar(query)

        if telegram_id is not None:
            raise TelegramIDError(f'Telegram ID: "{telegram_id}" уже зарегистрирован',
                                  status=HTTPStatus.CONFLICT)

        token = TokenWorker.generate_new_token()
        stmt = insert(User).values(**dict(user), token=token)

        await session.execute(stmt)
        await session.commit()

        return token

    @classmethod
    async def create_platoon(cls, platoon: Platoon, session: AsyncSession):
        stmt = insert(Platoon).values(**dict(platoon))

        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_platoon(cls, platoon_number: int, session: AsyncSession) -> dict:
        query = select(Platoon).where(Platoon.platoon_number == platoon_number)

        platoon = await session.scalar(query)
        await session.commit()

        return platoon.as_dict()

    @classmethod
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
