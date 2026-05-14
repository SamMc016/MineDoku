"""empty message

Revision ID: 6ab138156670
Revises: 47c0324d5e3a
Create Date: 2026-05-14 15:16:09.808522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ab138156670'
down_revision = '47c0324d5e3a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('friends')


def downgrade():
    op.create_table('friends',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('friend_username', sa.String(length=20), nullable=False),
    sa.Column('friend_daily_uniqueness', sa.Integer(), nullable=True),
    sa.Column('friend_all_time_uniqueness', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['friend_username'], ['user.username'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'friend_username')
    )
