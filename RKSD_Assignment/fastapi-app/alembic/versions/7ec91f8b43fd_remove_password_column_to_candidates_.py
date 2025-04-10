"""Remove password column to candidates table

Revision ID: 7ec91f8b43fd
Revises: 7678168d157f
Create Date: 2025-03-21 22:26:30.783799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ec91f8b43fd'
down_revision: Union[str, None] = '7678168d157f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('candidates', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidates', sa.Column('password', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###
