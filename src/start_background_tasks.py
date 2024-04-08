from services.tasks.tasks import set_attend_all_students_by_weekday, answer_platoon_about_attend


def start():
    set_attend_all_students_by_weekday.delay()
    answer_platoon_about_attend.delay()


if __name__ == '__main__':
    start()
