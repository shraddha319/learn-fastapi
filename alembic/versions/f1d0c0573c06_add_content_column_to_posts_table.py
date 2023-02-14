"""add content column to posts table

Revision ID: f1d0c0573c06
Revises: 887309562301
Create Date: 2023-02-14 21:17:09.300889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1d0c0573c06'
down_revision = '887309562301'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
