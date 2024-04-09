import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Attend
from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.ATTEND.key}") != "{Options.ATTEND.default_value}"'
)
class TestAttends:
    async def test_confirmation_attend_user(
            self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        query = select(Attend.id).limit(1)

        id_: int = await tst_async_session.scalar(query)

        response = await ac.patch(
            url="/attends/confirmation_attend_user",
            json={"id": id_, "confirmed": True},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201

    async def test_confirmation_attend_user_error(self, ac: AsyncClient, jwt_token):
        response = await ac.patch(
            url="/attends/confirmation_attend_user",
            json={"id": -1, "confirmed": True},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404
