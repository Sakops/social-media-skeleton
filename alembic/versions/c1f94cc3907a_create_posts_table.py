"""create posts table

Revision ID: c1f94cc3907a
Revises: 
Create Date: 2022-01-29 22:12:37.891234

"""
from contextlib import nullcontext
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1f94cc3907a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column(
        'id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
