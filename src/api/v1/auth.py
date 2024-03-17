from fastapi import APIRouter, Depends
from fastapi_users.authentication import JWTStrategy

from services.auth.auth import auth_user, auth_backend, get_jwt_strategy

current_user = auth_user.current_user()
router = APIRouter()


@router.post("/refresh")
async def refresh_jwt(
        jwt_strategy: JWTStrategy = Depends(get_jwt_strategy),
        user=Depends(current_user)
):
    return await auth_backend.login(jwt_strategy, user)
