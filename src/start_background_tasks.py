from services.tasks.tasks import set_attend_all_students_by_weekday


def start():
    set_attend_all_students_by_weekday.delay()


if __name__ == '__main__':
    start()
