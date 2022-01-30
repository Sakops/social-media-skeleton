"""add content column'

Revision ID: 5fa5ac793792
Revises: c1f94cc3907a
Create Date: 2022-01-29 22:21:55.403617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fa5ac793792'
down_revision = 'c1f94cc3907a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
