"""edit user table

Revision ID: 786d061183e6
Revises: 74b98ace4656
Create Date: 2024-02-16 22:25:23.024522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '786d061183e6'
down_revision: Union[str, None] = '74b98ace4656'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'telegram_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_unique_constraint(None, 'user', ['telegram_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.alter_column('user', 'telegram_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
