import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Subject
from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.SUBJECT.key}") != "{Options.SUBJECT.default_value}"'
)
class TestSubject:
    async def test_get_subjects(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        for i in range(3):
            stmt = insert(Subject).values(
                name=f"Test Subject_{i}",
                admin_id=0,
                platoon_id=0,
                semester=1,
            )
            await tst_async_session.execute(stmt)
            await tst_async_session.commit()

        response = await ac.get(
            url="/subject/get_subject_by_semester",
            params={"platoon_number": 0, "semester": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "1": {
                "id": 1,
                "platoon_id": 0,
                "semester": 1,
                "admin_id": 1,
                "name": "subject",
            },
            "2": {
                "id": 2,
                "platoon_id": 0,
                "semester": 1,
                "admin_id": 0,
                "name": "Test Subject_0",
            },
            "3": {
                "id": 3,
                "platoon_id": 0,
                "semester": 1,
                "admin_id": 0,
                "name": "Test Subject_1",
            },
            "4": {
                "id": 4,
                "platoon_id": 0,
                "semester": 1,
                "admin_id": 0,
                "name": "Test Subject_2",
            },
        }

    async def test_get_subjects_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/subject/get_subjects",
            params={"platoon_number": 352, "semester": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_gradings_by_student_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/subject/get_gradings_by_student",
            params={"user_id": 1, "subject_id": 9129},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

        response = await ac.get(
            url="/subject/get_gradings_by_student",
            params={"user_id": 2356, "subject_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_gradings_by_student(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/subject/get_gradings_by_student",
            params={"user_id": 1, "subject_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "2": {
                "id": 2,
                "mark": 1,
                "mark_date": f"{datetime.date.today()}",
                "theme": "Test theme",
            },
            "1": {"id": 1, "mark": 1, "mark_date": "2023-12-22", "theme": "theme"},
        }

    async def test_get_subject_by_now_semester(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        stmt = insert(Subject).values(
            name=f"Test Subject_818",
            admin_id=0,
            platoon_id=818,
            semester=2,
        )
        await tst_async_session.execute(stmt)
        await tst_async_session.commit()

        response = await ac.get(
            url="/subject/get_subject_by_now_semester",
            params={"platoon_number": 818},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "5": {
                "id": 5,
                "platoon_id": 818,
                "semester": 2,
                "admin_id": 0,
                "name": "Test Subject_818",
            }
        }

    async def test_get_subject_by_semester(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        stmt = insert(Subject).values(
            name=f"Test Subject_818",
            admin_id=0,
            platoon_id=818,
            semester=1,
        )

        await tst_async_session.execute(stmt)
        await tst_async_session.commit()

        response = await ac.get(
            url="/subject/get_subject_by_semester",
            params={"platoon_number": 818, "semester": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "6": {
                "id": 6,
                "platoon_id": 818,
                "semester": 1,
                "admin_id": 0,
                "name": "Test Subject_818",
            }
        }

    async def test_create_subject(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/subject/create_subject",
            params={
                "platoon_number": 818,
                "semester": 1,
                "subject_name": "Test subject",
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == 7

    @pytest.mark.parametrize(
        ["platoon_number", "semester", "subject_name", "status_code"],
        [
            (-1, 1, "Test subject", 404),
            (818, -1, "Test subject", 400),
        ],
    )
    async def test_create_subject_error(
        self,
        ac: AsyncClient,
        jwt_token,
        platoon_number,
        semester,
        subject_name,
        status_code,
    ):
        response = await ac.post(
            url="/subject/create_subject",
            params={
                "platoon_number": platoon_number,
                "semester": semester,
                "subject_name": subject_name,
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == status_code
