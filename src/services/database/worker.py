from http import HTTPStatus
from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select, func, and_, update, exists
from sqlalchemy.ext.asyncio import AsyncSession

from config import Roles
from exceptions import PlatoonError, UserNotFound, UserError, SubjectError
from models import User, Platoon, Subject, Attend, Grading
from models.view.users import Users
from schemas.platoon import PlatoonDTO
from services.database.connector import BaseTable, get_async_session


class DatabaseWorker:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_platoon(self, platoon_number: int):
        if not await self.platoon_number_is_exist(platoon_number):
            raise PlatoonError(
                message="Platoon not found", status_code=HTTPStatus.NOT_FOUND
            )

        query = select(User).where(platoon_number == User.platoon_number)

        users = await self.session.scalars(query)
        await self.session.commit()

        result = users.all()

        return result

    async def get_platoons(self):
        query = select(Platoon)

        platoons = await self.session.scalars(query)

        return platoons

    async def get_attendance_status_user(self, user_id):
        if not await self.user_is_exist(user_id):
            raise UserNotFound(
                message="Данного пользователя не существует",
                status_code=HTTPStatus.NOT_FOUND
            )

        query = (
            select(Attend).
            where(Attend.user_id == user_id)
        )

        attendances = await self.session.scalars(query)

        return attendances

    async def get_gradings_by_student(self, user_id: int, subject_id: int):
        if not await self.user_is_exist(user_id):
            raise UserError(
                message="Пользователя не существует",
                status_code=HTTPStatus.NOT_FOUND
            )
        if not await self.subject_is_exist(subject_id):
            raise SubjectError(
                message="Данного предмета не существует",
                status_code=HTTPStatus.NOT_FOUND
            )

        query = (
            select(Grading).
            where(
                and_(
                    Grading.user_id == user_id,
                    Grading.subj_id == subject_id
                )
            )
        )

        gradings = await self.session.scalars(query)

        return gradings

    async def get_students_list(self):
        query = select(User).where(User.role.not_in([Roles.admin, Roles.professor]))

        students = await self.session.scalars(query)

        return students

    async def get_professors_list(self):
        query = select(User).where(User.role == Roles.professor)

        students = await self.session.scalars(query)

        return students

    async def set_visit_user(self, date_v: str, visiting: int, user_id: int):
        if not await self.user_is_exist(user_id):
            raise UserNotFound(status_code=HTTPStatus.NOT_FOUND)

        query = select(Users.c.course_number).where(Users.c.id == user_id)

        semester = await self.session.scalar(query)

        is_exist_query = (
            exists(Attend.id)
            .where(and_(Attend.user_id == user_id, Attend.date_v == date_v))
            .select()
        )

        is_exist = await self.session.scalar(is_exist_query)

        if not is_exist:
            stmt = insert(Attend).values(
                user_id=user_id, date_v=date_v, visiting=visiting, semester=semester
            )
        else:
            stmt = update(Attend).values(
                user_id=user_id, date_v=date_v, visiting=visiting, semester=semester
            )

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_tg_from_id(self, telegram_id: int):
        query = select(User.id).where(User.telegram_id == telegram_id)

        telegram_id = await self.session.scalar(query)
        await self.session.commit()

        return telegram_id

    async def get_semesters(self, user_id: int) -> dict[str, Sequence]:
        sub_query = (
            select(User.platoon_number).where(User.id == user_id)
        ).scalar_subquery()

        query = (
            select(Subject.semester)
            .where(Subject.platoon_id == sub_query)
            .group_by(Subject.semester)
        )

        semesters = await self.session.scalars(query)
        await self.session.commit()

        return {"semesters": semesters.all()}

    async def get_subjects(self, platoon_number: int, semester: int):
        if not await self.platoon_number_is_exist(platoon_number):
            raise PlatoonError(
                message="Platoon not found", status_code=HTTPStatus.NOT_FOUND
            )

        query = select(Subject).filter_by(platoon_id=platoon_number, semester=semester)

        subjects = await self.session.scalars(query)

        return subjects

    async def get_user_role(self, user_id: int) -> str:
        if not await self.user_is_exist(user_id):
            raise UserNotFound(
                message=f"User {user_id=} not found", status_code=HTTPStatus.NOT_FOUND
            )

        query = select(User).where(User.id == user_id)
        user = await self.session.scalar(query)

        return user.convert_to_dict()["role"]

    async def get_user(self, user_id: int) -> User:
        if not await self.user_is_exist(user_id):
            raise UserNotFound(
                message=f"User {user_id=} not found", status_code=HTTPStatus.NOT_FOUND
            )

        query = select(User).filter_by(id=user_id)

        user = await self.session.scalar(query)

        return user

    async def get_user_by_tg(self, telegram_id: int) -> User:
        query = select(User).filter_by(telegram_id=telegram_id)

        user = await self.session.scalar(query)

        if not user:
            raise UserNotFound(
                message=f"User {telegram_id=} not found",
                status_code=HTTPStatus.NOT_FOUND,
            )

        return user

    async def set_user_attr(self, user_id: int, **kwargs):
        stmt = update(User).values(**kwargs).where(User.id == user_id)

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_platoon_commander(self, platoon_number: int) -> dict:
        query = select(User).where(
            and_(
                User.role == Roles.platoon_commander,
                User.platoon_number == platoon_number,
            )
        )

        commander = await self.session.scalar(query)
        await self.session.commit()

        if commander is None:
            raise PlatoonError(
                message=f'Командир во взводе "{platoon_number}" не найден',
                status_code=HTTPStatus.NOT_FOUND,
            )

        return commander.convert_to_dict()

    async def create_platoon(self, platoon: PlatoonDTO):
        if await self.platoon_number_is_exist(platoon.platoon_number):
            raise PlatoonError(
                f"{platoon.platoon_number=} already exist",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        stmt = insert(Platoon).values(**dict(platoon))

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_count_squad_in_platoon(self, platoon_number: int) -> int:
        if not await self.platoon_number_is_exist(platoon_number):
            raise PlatoonError(
                message="Platoon not found", status_code=HTTPStatus.NOT_FOUND
            )

        query = select(func.sum(1)).select_from(
            select(User.squad_number)
            .where(
                and_(
                    User.platoon_number == platoon_number,
                    User.squad_number.in_([1, 2, 3]),
                )
            )
            .group_by(User.squad_number)
            .subquery()
        )

        count = await self.session.scalar(query)
        await self.session.commit()

        return count

    async def user_is_exist(self, user_id: int) -> bool:
        return await self._check_exist_entity(User, user_id)

    async def telegram_id_is_exist(self, telegram_id: int) -> bool:
        return await self._check_exist_entity_column(
            User, {User.telegram_id.name: telegram_id}
        )

    async def email_is_exist(self, email: str) -> bool:
        return await self._check_exist_entity_column(User, {User.email.name: email})

    async def platoon_number_is_exist(self, platoon_number: int) -> bool:
        query = exists(Platoon).where(Platoon.platoon_number == platoon_number).select()

        is_exist = await self.session.scalar(query)

        return is_exist

    async def subject_is_exist(self, subject_id: int) -> bool:
        query = exists(Subject).where(Subject.id == subject_id).select()

        is_exist = await self.session.scalar(query)

        return is_exist

    async def platoon_commander_is_exist(self, platoon_number: int) -> bool:
        query = (
            exists(User)
            .where(
                and_(
                    User.platoon_number == platoon_number,
                    User.role == Roles.platoon_commander,
                )
            )
            .select()
        )

        return await self.session.scalar(query)

    async def _check_exist_entity(self, entity: BaseTable, entity_id) -> bool:
        ent = await self.session.get(entity, entity_id)

        if ent is not None:
            return True

        return False

    async def _check_exist_entity_column(
            self, entity: BaseTable, columns: dict
    ) -> bool:
        query = select(entity).filter_by(**columns)
        res = await self.session.scalar(query)

        if res is not None:
            return True

        return False


async def get_database_worker(session: AsyncSession = Depends(get_async_session)):
    yield DatabaseWorker(session)
