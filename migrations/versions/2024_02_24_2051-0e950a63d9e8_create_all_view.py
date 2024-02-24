"""create all view

Revision ID: 0e950a63d9e8
Revises: ed610cef02cf
Create Date: 2024-02-24 20:51:42.211876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models.view.attendance import Attendance
from models.view.marks import Marks
from models.view.platoons import Platoons
from models.view.students import Students
from models.view.users import Users

# revision identifiers, used by Alembic.
revision: str = '0e950a63d9e8'
down_revision: Union[str, None] = 'ed610cef02cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Attendance.create(op)
    Marks.create(op)
    Platoons.create(op)
    Students.create(op)
    Users.create(op)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Attendance.drop(op)
    Marks.drop(op)
    Platoons.drop(op)
    Students.drop(op)
    Users.drop(op)
    # ### end Alembic commands ###