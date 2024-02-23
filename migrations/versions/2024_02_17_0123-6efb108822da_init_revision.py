"""init revision

Revision ID: 6efb108822da
Revises: 
Create Date: 2024-02-17 01:23:11.363534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6efb108822da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('day',
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('weekday', sa.Integer(), nullable=False),
    sa.Column('semester', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('date')
    )
    op.create_table('platoon',
    sa.Column('platoon_number', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vus', sa.Integer(), nullable=False),
    sa.Column('semester', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('platoon_number')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('mail', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('institute', sa.String(), nullable=True),
    sa.Column('direction_of_study', sa.String(), nullable=True),
    sa.Column('group_study', sa.String(), nullable=True),
    sa.Column('platoon_number', sa.Integer(), nullable=True),
    sa.Column('vus', sa.Integer(), nullable=True),
    sa.Column('squad_number', sa.Integer(), nullable=True),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('platoon_id', sa.Integer(), nullable=False),
    sa.Column('semester', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['platoon_id'], ['platoon.platoon_number'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('mail', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('institute', sa.String(), nullable=True),
    sa.Column('direction_of_study', sa.String(), nullable=True),
    sa.Column('platoon_number', sa.Integer(), nullable=True),
    sa.Column('squad_number', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(), nullable=True, default='Студент'),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('group_study', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['platoon_number'], ['platoon.platoon_number'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('attend',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_v', sa.Date(), nullable=False),
    sa.Column('visiting', sa.Integer(), nullable=True),
    sa.Column('semester', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grading',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subj_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('mark', sa.Integer(), nullable=False),
    sa.Column('mark_date', sa.Date(), nullable=False),
    sa.Column('theme', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['subj_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message_queue',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['telegram_id'], ['user.telegram_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_queue')
    op.drop_table('grading')
    op.drop_table('attend')
    op.drop_table('user')
    op.drop_table('subject')
    op.drop_table('students')
    op.drop_table('platoon')
    op.drop_table('day')
    op.drop_table('admins')
    # ### end Alembic commands ###
