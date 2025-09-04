"""group_role enum + role column + migrate admins to group_members"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Alembic ids
revision: str = "e91d4c8d2834"
down_revision: Union[str, None] = "20250832"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Bezpieczne CREATE TYPE (nie wywali, jeśli typ już istnieje)
    op.execute("""
    DO $$ BEGIN
        CREATE TYPE group_role AS ENUM ('MEMBER','ADMIN');
    EXCEPTION
        WHEN duplicate_object THEN NULL;
    END $$;
    """)

    op.add_column(
        "group_members",
        sa.Column(
            "role",
            postgresql.ENUM("MEMBER", "ADMIN", name="group_role", create_type=False),
            nullable=False,
            server_default="MEMBER",
        ),
    )

    # legacy tabele out
    op.execute("DROP TABLE IF EXISTS admins CASCADE")
    op.execute("DROP TABLE IF EXISTS university_admins CASCADE")
    # legacy enum po tabeli
    op.execute("DROP TYPE IF EXISTS university_role")

    # (opcjonalnie) usun server_default, zostawiając NOT NULL
    op.alter_column("group_members", "role", server_default=None)


def downgrade() -> None:
    # najpierw kolumna, potem typ (odwrotna kolejnosc niz w upgrade)
    with op.batch_alter_table("group_members") as batch_op:
        batch_op.drop_column("role")

    # nie uzywaj CASCADE na typie, zeby nie skasowac czegos przypadkiem
    op.execute("DROP TYPE IF EXISTS group_role")
    # celowo nie odtwarzamy admins/university_admins
