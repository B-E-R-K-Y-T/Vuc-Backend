from httpx import AsyncClient


async def test_create_platoon(ac: AsyncClient, jwt_token):
    response = await ac.post(
        "/platoons/create",
        json={"platoon_number": 818, "vus": 818, "semester": 818},
        cookies={"bonds": jwt_token},
    )

    assert response.status_code == 201
    assert response.json() == {"platoon_number": 818}
