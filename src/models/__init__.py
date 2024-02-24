# Эти импорты заполняют переменную Base, в которой лежат метаданные, это нужно, чтобы модели были видны при миграциях
from models.student import Student
from models.admin import Admin
from models.day import Day
from models.attend import Attend
from models.grading import Grading
from models.message_queue import MessageQueue
from models.user import User
from models.platoon import Platoon
from models.subject import Subject
