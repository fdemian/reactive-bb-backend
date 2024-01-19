"""Add banfields.

Revision ID: 35857e77badf
Revises: aaae56500290
Create Date: 2023-01-16 12:12:19.548761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "35857e77badf"
down_revision = "aaae56500290"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users", sa.Column("banned", sa.Boolean, nullable=False, server_default="False")
    )
    op.add_column("users", sa.Column("ban_reason", sa.Text, nullable=True))


def downgrade():
    op.drop_column("users", "banned")
    op.drop_column("users", "ban_reason")
