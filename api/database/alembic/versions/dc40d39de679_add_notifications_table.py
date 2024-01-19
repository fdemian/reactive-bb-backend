"""Add notifications table.

Revision ID: dc40d39de679
Revises: 47226b88abf0
Create Date: 2022-09-21 08:56:47.640457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dc40d39de679"
down_revision = "47226b88abf0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("link", sa.Text, nullable=False),
        sa.Column("user", sa.Integer, nullable=False),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("read", sa.Boolean, nullable=False, default=False),
    )


def downgrade():
    op.drop_table("notifications")
