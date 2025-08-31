from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

revision = "20250832"
down_revision = "20250831"  # <- zostaw, jeśli poprzednia migracja ma revision=20250831
branch_labels = None
depends_on = None

def upgrade():
    # 1) Utwórz typ TYLKO jeśli nie istnieje (Postgres nie ma CREATE TYPE IF NOT EXISTS)
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'invite_status') THEN
            CREATE TYPE invite_status AS ENUM ('PENDING','ACCEPTED','DECLINED','CANCELED','EXPIRED');
        END IF;
    END$$;
    """)

    # 2) Użyj istniejącego już typu – nie twórz go ponownie
    invite_status = pg.ENUM(
        'PENDING','ACCEPTED','DECLINED','CANCELED','EXPIRED',
        name='invite_status', create_type=False
    )

    op.create_table(
        "group_invitations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id", ondelete="CASCADE"), nullable=False),
        sa.Column("invited_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("inviter_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", invite_status, nullable=False,
                  server_default=sa.text("'PENDING'::invite_status")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        # opcjonalnie:
        # sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    op.create_index(op.f("ix_group_invitations_group_id"), "group_invitations", ["group_id"])
    op.create_index(op.f("ix_group_invitations_invited_user_id"), "group_invitations", ["invited_user_id"])

    op.create_index(
        "uq_group_invitations_pending",
        "group_invitations",
        ["group_id", "invited_user_id"],
        unique=True,
        postgresql_where=sa.text("status = 'PENDING'")
    )

def downgrade():
    op.drop_index("uq_group_invitations_pending", table_name="group_invitations")
    op.drop_index(op.f("ix_group_invitations_invited_user_id"), table_name="group_invitations")
    op.drop_index(op.f("ix_group_invitations_group_id"), table_name="group_invitations")
    op.drop_table("group_invitations")
    op.execute("DROP TYPE IF EXISTS invite_status;")
