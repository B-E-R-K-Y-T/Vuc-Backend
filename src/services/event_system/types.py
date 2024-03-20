import hashlib

from services.util import CollectorField


class _auto_event:
    event_idx: int = 0

    def __new__(cls, *args, **kwargs):
        cls.event_idx += 1

        return hashlib.md5(bytes(cls.event_idx)).hexdigest()


class Event(str):
    pass


class EventFilter(CollectorField):
    field_type = Event


class TypeEvent(EventFilter):
    MESSAGE_TO_SPECIFIC_USER: Event = _auto_event()
