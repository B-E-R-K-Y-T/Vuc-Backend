from http import HTTPStatus


class MainVucException(Exception):
    def __init__(self, *args, status=HTTPStatus.INTERNAL_SERVER_ERROR, **kwargs):
        super().__init__(*args, **kwargs)

        self.__status = status
        if args:
            self.__message = args[0]
        else:
            self.__message = f'Unknown error. Detail: {self.__status=}: {self.__class__=}'

    def __str__(self):
        return self.__message

    @property
    def status(self):
        return self.__status


class TelegramIDError(MainVucException):
    pass


class PlatoonError(MainVucException):
    pass


class RoleError(MainVucException):
    pass