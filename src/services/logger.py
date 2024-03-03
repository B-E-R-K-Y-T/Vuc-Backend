import logging
from logging.handlers import RotatingFileHandler

from config import BASE_DIR

_FILE_NAME = f"{BASE_DIR}/vuc_backend_app-log.log"
_LOG_MODE = logging.DEBUG


class Logger:
    def __init__(self, file_name=_FILE_NAME):
        self.__logger = logging.getLogger()
        self.__logger.setLevel(_LOG_MODE)

        handler = RotatingFileHandler(
            filename=file_name, maxBytes=1024**2, backupCount=3
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s: %(name)s - %(levelname)s - %(message)s")
        )
        self.__logger.addHandler(handler)

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
    "LOGGER",
)
