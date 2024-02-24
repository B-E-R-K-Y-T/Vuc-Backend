import logging

from config import BASE_DIR

_FILE_NAME = f'{BASE_DIR}/vuc_backend_app-log.log'
_LOG_MODE = logging.DEBUG


class Logger:
    def __init__(self, file_name=_FILE_NAME):
        logging.basicConfig(
            filename=file_name,
            filemode='a',
            format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
            level=_LOG_MODE
        )
        self.__logger = logging.getLogger()

    def warn(self, *args, **kwargs):
        self.__logger.warning(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.__logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.__logger.info(*args, **kwargs)

    def err(self, *args, **kwargs):
        self.__logger.error(*args, **kwargs)


LOGGER = Logger()

__all__ = (
    Logger.__name__,
    'LOGGER',
)
