from typing import Callable, Awaitable, Optional

from exceptions import EventErrorException
from services.util import sync_async_call


class EventBus:
    __events: dict = {}

    @classmethod
    def subscribe_event(
            cls,
            event,
            func: Callable | Awaitable,
            args: Optional[tuple] = (),
            kwargs: Optional[dict] = {}
    ):
        functions: list = cls.__events.get(event)

        if functions is None:
            cls.__events[event] = [{"func": func, "args": args, "kwargs": kwargs}]
        else:
            functions.append({"func": func, "args": args, "kwargs": kwargs})

    @classmethod
    def event_is_exist(cls, event) -> bool:
        return cls.__events.get(event) is not None

    @classmethod
    def bind(cls, event):
        def decorator(func: Callable | Awaitable):
            cls.subscribe_event(event, func)

            return func

        return decorator

    @classmethod
    async def dispatch(cls, event, *args, **kwargs):
        functions_image: list[dict] = cls.__events.pop(event)

        if functions_image is None:
            raise EventErrorException(f'Unknown event: "{event}"')

        for function_image in functions_image:
            await sync_async_call(
                function_image["func"],
                *function_image["args"],
                *args,
                **kwargs,
                **function_image["kwargs"]
            )
