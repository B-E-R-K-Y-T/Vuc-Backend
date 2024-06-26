"""deleted student table

Revision ID: eed93646d0a4
Revises: f95ccf8ffcae
Create Date: 2024-04-18 19:47:40.328234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eed93646d0a4"
down_revision: Union[str, None] = "f95ccf8ffcae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("student")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "student",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "name", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.Column(
            "phone",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "date_of_birth", sa.DATE(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "mail", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.Column(
            "address",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "institute",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "direction_of_study",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "group_study",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "platoon_number", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("vus", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "squad_number", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "telegram_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "token",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "role", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="student_pkey"),
    )
    # ### end Alembic commands ###
