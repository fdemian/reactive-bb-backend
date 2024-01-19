"""Add moderator types.

Revision ID: aaae56500290
Revises: 9145934226c3
Create Date: 2023-01-04 16:48:20.556807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aaae56500290"
down_revision = "9145934226c3"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("topics", "active")
    op.add_column(
        "topics",
        sa.Column("closed", sa.Boolean, nullable=False, server_default="False"),
    )
    op.add_column(
        "users", sa.Column("type", sa.Unicode(1), nullable=False, server_default="U")
    )


def downgrade():
    op.drop_column("topics", "closed")
    op.add_column("topics", sa.Column("active", sa.Boolean, nullable=True))
    op.drop_column("users", "type")
