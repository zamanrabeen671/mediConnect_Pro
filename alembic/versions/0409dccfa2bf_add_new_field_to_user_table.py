"""Add new_field to user table

Revision ID: 0409dccfa2bf
Revises: 
Create Date: 2025-12-25 21:14:11.566832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0409dccfa2bf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add phone column to users table
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    # Create unique constraint on phone column
    op.create_unique_constraint('uq_users_phone', 'users', ['phone'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop unique constraint first
    op.drop_constraint('uq_users_phone', 'users', type_='unique')
    # Then drop the column
    op.drop_column('users', 'phone')