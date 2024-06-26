"""telegram_id in user is nullable

Revision ID: b6245cd1a3b6
Revises: eed93646d0a4
Create Date: 2024-05-09 14:49:29.852331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6245cd1a3b6"
down_revision: Union[str, None] = "eed93646d0a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user", "telegram_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user", "telegram_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###
