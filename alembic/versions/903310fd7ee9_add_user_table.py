"""add user table

Revision ID: 903310fd7ee9
Revises: 5fa5ac793792
Create Date: 2022-01-29 22:26:37.583363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '903310fd7ee9'
down_revision = '5fa5ac793792'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('name', sa.String(), nullable=False), sa.Column('email', sa.String(), nullable=False, unique=True), sa.Column('password', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('users')
    pass
