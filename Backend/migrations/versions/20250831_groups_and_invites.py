from alembic import op
import sqlalchemy as sa

revision = '20250831'
down_revision = '869321ae1320'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'group_members',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index(op.f('ix_group_members_user_id'), 'group_members', ['user_id'])
    op.create_index(op.f('ix_group_members_group_id'), 'group_members', ['group_id'])

def downgrade():
    op.drop_index(op.f('ix_group_members_group_id'), table_name='group_members')
    op.drop_index(op.f('ix_group_members_user_id'), table_name='group_members')
    op.drop_table('group_members')
