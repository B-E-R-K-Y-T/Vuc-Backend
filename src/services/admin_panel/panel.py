from sqladmin import ModelView

from models import *
from .model_worker import ModelCollector

_model_collector = ModelCollector()


@_model_collector.bind_model
class _UserTable(ModelView, model=User):
    column_list = [User.id, User.name]
    form_ajax_refs = {"platoon": {"fields": (Platoon.platoon_number,)}}


@_model_collector.bind_model
class _StudentTable(ModelView, model=Student):
    column_list = [Student.id, Student.name]


@_model_collector.bind_model
class _DayTable(ModelView, model=Day):
    column_list = [Day.date]


@_model_collector.bind_model
class _AttendTable(ModelView, model=Attend):
    column_list = [Attend.id, Attend.user_id, Attend.date_v]
    form_ajax_refs = {"user": {"fields": (User.id, User.name, User.platoon_number)}}


@_model_collector.bind_model
class _GradingTable(ModelView, model=Grading):
    column_list = [Grading.id, Grading.subj_id, Grading.mark, Grading.theme]
    form_ajax_refs = {
        "subject": {"fields": (Subject.id, Subject.name)},
        "user": {"fields": (User.id, User.name)},
    }


@_model_collector.bind_model
class _MessageQueueTable(ModelView, model=MessageQueue):
    column_list = [MessageQueue.id, MessageQueue.message]


@_model_collector.bind_model
class _SubjectTable(ModelView, model=Subject):
    column_list = [Subject.id, Subject.name]
    form_ajax_refs = {"platoon": {"fields": (Platoon.platoon_number,)}}


@_model_collector.bind_model
class _PlatoonTable(ModelView, model=Platoon):
    column_list = [Platoon.platoon_number]
    form_include_pk = True


@_model_collector.bind_model
class _AdminTable(ModelView, model=Admin):
    column_list = [Admin.name]


@_model_collector.bind_model
class _ScheduleTable(ModelView, model=Schedule):
    column_list = [Schedule.id, Schedule.day, Schedule.platoon_number]
    form_ajax_refs = {
        "platoon": {"fields": (Platoon.platoon_number,)},
        "day": {"fields": (Day.id,)},
    }


MODELS = _model_collector.models


def init_admin_panel(app, engine):
    from sqladmin import Admin
    from .auth import AdminPanelAuth

    authentication_backend = AdminPanelAuth()
    administrator = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend
    )

    for model in sorted(MODELS, key=lambda model_: model_.__name__):
        administrator.add_view(model)

    return administrator


__all__ = (
    init_admin_panel.__name__,
    "MODELS"
)
