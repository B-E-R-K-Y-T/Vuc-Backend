"""add view users

Revision ID: f657ce76a7ee
Revises: 5ecfcdde3087
Create Date: 2024-02-23 18:25:05.128028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models.view.users import Users

# revision identifiers, used by Alembic.
revision: str = 'f657ce76a7ee'
down_revision: Union[str, None] = '5ecfcdde3087'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Users.create(op)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Users.drop(op)
    # ### end Alembic commands ###