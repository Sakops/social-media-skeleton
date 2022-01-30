"""adding foreign key to posts

Revision ID: 54fd87c2abc0
Revises: 903310fd7ee9
Create Date: 2022-01-29 22:49:49.524622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54fd87c2abc0'
down_revision = '903310fd7ee9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'poster_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'poster_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'poster_id')
    pass
