"""cascade admins on group delete

Revision ID: 869321ae1320
Revises: 6a55f17835ca
Create Date: 2025-08-29 20:57:46.856466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '869321ae1320'
down_revision: Union[str, None] = '6a55f17835ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
