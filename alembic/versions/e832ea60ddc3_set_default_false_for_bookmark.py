"""set default false for bookmark

Revision ID: e832ea60ddc3
Revises: 0309a7dd584f
Create Date: 2026-04-17 10:14:36.175981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e832ea60ddc3'
down_revision: Union[str, Sequence[str], None] = '0309a7dd584f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'notes',
        'bookmark',
        server_default=sa.text('false')
    )

    op.execute(
        "UPDATE notes SET bookmark = false WHERE bookmark IS NULL"
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'notes',
        'bookmark',
        server_default=None
    )
