"""add content column to posts table

Revision ID: 64d3358170d9
Revises: 8b6b7a08cb9f
Create Date: 2023-04-04 21:56:13.348132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d3358170d9'
down_revision = '8b6b7a08cb9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
