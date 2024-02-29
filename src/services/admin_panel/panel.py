from sqladmin import ModelView

from models import *
from .model_builder import ModelCollector
from .auth import AdminAuth

_model_collector = ModelCollector()


@_model_collector.target_model()
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]


@_model_collector.target_model()
class StudentAdmin(ModelView, model=Student):
    column_list = [Student.id, Student.name]


@_model_collector.target_model()
class DayAdmin(ModelView, model=Day):
    column_list = [Day.date]


@_model_collector.target_model()
class AttendAdmin(ModelView, model=Attend):
    column_list = [Attend.id, Attend.user_id, Attend.date_v]


@_model_collector.target_model()
class GradingAdmin(ModelView, model=Grading):
    column_list = [Grading.id, Grading.subj_id, Grading.mark, Grading.theme]


@_model_collector.target_model()
class MessageQueueAdmin(ModelView, model=MessageQueue):
    column_list = [MessageQueue.id, MessageQueue.message]


@_model_collector.target_model()
class SubjectAdmin(ModelView, model=Subject):
    column_list = [Subject.id, Subject.name]


@_model_collector.target_model()
class PlatoonAdmin(ModelView, model=Platoon):
    column_list = [Platoon.platoon_number]


ADMIN_MODELS = _model_collector.models


def init_admin_panel(app, engine):
    from sqladmin import Admin

    authentication_backend = AdminAuth()
    administrator = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

    for model in ADMIN_MODELS:
        administrator.add_view(model)

    return administrator
