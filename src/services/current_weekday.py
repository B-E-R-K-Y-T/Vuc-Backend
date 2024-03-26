import datetime


class Day:
    def __init__(self, name: str, number: int):
        self.__name = name
        self.__number = number

    @property
    def name(self):
        return self.name

    @property
    def number(self):
        return self.__number


class WeekDays:
    MONDAY = Day("Понедельник", 1)
    TUESDAY = Day("Вторник", 2)
    WEDNESDAY = Day("Среда", 3)
    THURSDAY = Day("Четверг", 4)
    FRIDAY = Day("Пятница", 5)
    SATURDAY = Day("Суббота", 6)
    SUNDAY = Day("Воскресенье", 7)


def get_current_day_of_the_week() -> Day:
    days = (
        WeekDays.MONDAY,
        WeekDays.TUESDAY,
        WeekDays.WEDNESDAY,
        WeekDays.THURSDAY,
        WeekDays.FRIDAY,
        WeekDays.SATURDAY,
        WeekDays.SUNDAY
    )
    today = datetime.datetime.today().weekday()

    return days[today]
