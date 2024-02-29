import secrets

from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request

from config import app_settings


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str = None):
        if secret_key is None:
            super().__init__(secret_key=secrets.token_hex(16))
        else:
            super().__init__(secret_key=secret_key)

        self.tokens = []

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not username or not password:
            return False

        if username != app_settings.LOGIN_ADMIN_PANEL:
            return False

        if password != app_settings.PASSWORD_ADMIN_PANEL:
            return False

        token = secrets.token_hex(16)
        request.session.update({"token": token})

        self.tokens.append(token)

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        token = request.session.get("token")

        if token is not None:
            self.tokens.remove(token)

        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        for t in self.tokens:
            if t == token:
                return True

        return False
