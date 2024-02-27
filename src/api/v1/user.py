from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from services.auth.auth import auth_user
from services.database.connector import get_async_session
from services.util import exception_handler
from services.database.worker import DatabaseWorker

current_user = auth_user.current_user()
router = APIRouter(
    prefix="/users",
)


@router.get("/admin-protected-route")
@exception_handler
async def admin_protected_route(user: User = Depends(auth_user.access_from_admin(current_user))):
    p = await DatabaseWorker.get_platoon(0)
    print(p.vus)

    return p


@router.get("/student-protected-route")
@exception_handler
async def student_protected_route(user: User = Depends(auth_user.access_from_student(current_user)),
                                  session: AsyncSession = Depends(get_async_session)):
    return f"Hello, {user.name}, {await DatabaseWorker(session).platoon_number_is_exist(23666660)}"
