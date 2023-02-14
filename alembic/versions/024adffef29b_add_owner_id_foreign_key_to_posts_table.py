"""add owner_id foreign key to posts table

Revision ID: 024adffef29b
Revises: c7af50dd4bd0
Create Date: 2023-02-14 21:35:46.541384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024adffef29b'
down_revision = 'c7af50dd4bd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_post_user_id',
                          source_table='posts', 
                          referent_table='users', 
                          local_cols=['owner_id'], 
                          remote_cols=['id'], 
                          ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('fk_post_user_id', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
