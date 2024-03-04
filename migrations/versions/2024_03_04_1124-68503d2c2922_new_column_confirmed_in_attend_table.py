"""new column confirmed in attend table

Revision ID: 68503d2c2922
Revises: cf8719f80d7a
Create Date: 2024-03-04 11:24:27.512398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "68503d2c2922"
down_revision: Union[str, None] = "cf8719f80d7a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "attend", sa.Column("confirmed", sa.Boolean(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("attend", "confirmed")
    # ### end Alembic commands ###
