"""
Эти исключения желательно должны возбуждаться только на ошибки со стороны клиента(не тот формат почты, или номер взвода).
Не стоит использовать их, чтобы маркировать ошибки на стороне сервера(5xx).
"""

from http import HTTPStatus


class MainVucException(Exception):
    def __init__(self, message=None, *args, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__(*args)

        self.__status_code = status_code
        if message is not None:
            self.__message = message
        else:
            self.__message = (
                f"Unknown error. Detail: {self.status_code=}: {self.__class__=}"
            )

    def __str__(self):
        return self.__message

    @property
    def status_code(self):
        return self.__status_code


class TelegramIDError(MainVucException):
    pass


class EmailError(MainVucException):
    pass


class PlatoonError(MainVucException):
    pass


class AttendError(MainVucException):
    pass


class SubjectError(MainVucException):
    pass


class UserError(MainVucException):
    pass


class SemesterError(MainVucException):
    pass


class EventErrorException(MainVucException):
    pass


class UserNotFound(UserError):
    def __init__(
        self,
        *args,
        message: str = "User not found",
        status_code=HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(*args, message=message, status_code=status_code)


class UserAlreadyExists(UserError):
    def __init__(
        self,
        *args,
        message: str = "The user already exists",
        status_code=HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(*args, message=message, status_code=status_code)
