"""add view students

Revision ID: 5ecfcdde3087
Revises: a6d39f3a73ac
Create Date: 2024-02-23 17:54:07.307871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.models.view.students import Students


# revision identifiers, used by Alembic.
revision: str = '5ecfcdde3087'
down_revision: Union[str, None] = 'a6d39f3a73ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Students.create(op)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Students.drop(op)
    # ### end Alembic commands ###
