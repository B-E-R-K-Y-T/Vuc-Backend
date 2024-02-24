"""add view marks

Revision ID: 01a15af02665
Revises: b91906e0c9e9
Create Date: 2024-02-23 17:29:45.010221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.models.view.marks import Marks

# revision identifiers, used by Alembic.
revision: str = '01a15af02665'
down_revision: Union[str, None] = 'b91906e0c9e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Marks.create(op)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Marks.drop(op)
    # ### end Alembic commands ###