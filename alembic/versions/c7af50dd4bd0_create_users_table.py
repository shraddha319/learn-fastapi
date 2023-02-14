"""create users table

Revision ID: c7af50dd4bd0
Revises: f1d0c0573c06
Create Date: 2023-02-14 21:24:03.505951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7af50dd4bd0'
down_revision = 'f1d0c0573c06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False), 
                    sa.Column('email', sa.String(), nullable=False, unique=True), 
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
