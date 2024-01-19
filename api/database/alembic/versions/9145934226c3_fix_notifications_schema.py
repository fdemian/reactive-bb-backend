"""Fix notifications schema.

Revision ID: 9145934226c3
Revises: f0e06b4cdd92
Create Date: 2022-10-27 20:47:36.333909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9145934226c3"
down_revision = "f0e06b4cdd92"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("notifications", "text")
    op.drop_column("notifications", "user")
    op.add_column(
        "notifications",
        sa.Column(
            "originator_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False
        ),
    )
    op.add_column(
        "notifications",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade():
    op.drop_column("notifications", "originator_id")
    op.drop_column("notifications", "user_id")
    op.add_column(
        "notifications", sa.Column("text", sa.Text, nullable=False, server_default="")
    )
    op.add_column("notifications", sa.Column("user", sa.Integer, nullable=True))
