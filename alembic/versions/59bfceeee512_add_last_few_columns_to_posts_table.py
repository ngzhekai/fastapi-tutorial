"""add last few columns to posts table

Revision ID: 59bfceeee512
Revises: f44644a46a30
Create Date: 2023-04-04 23:21:10.720727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59bfceeee512'
down_revision = 'f44644a46a30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
        ('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
