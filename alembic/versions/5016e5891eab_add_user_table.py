"""add user table

Revision ID: 5016e5891eab
Revises: 64d3358170d9
Create Date: 2023-04-04 22:46:55.636746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5016e5891eab'
down_revision = '64d3358170d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                   sa.Column('id', sa.Integer(), nullable=False),
                   sa.Column('email', sa.String(), nullable=False),
                   sa.Column('password', sa.String(), nullable=False),
                   sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                             server_default=sa.text('now()'), nullable=False),
                   sa.PrimaryKeyConstraint('id'),
                   sa.UniqueConstraint('email')
                   )

    pass

def downgrade() -> None:
    op.drop_table('users')
    pass
