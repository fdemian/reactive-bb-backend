"""Add chat table.

Revision ID: f0e06b4cdd92
Revises: dc40d39de679
Create Date: 2022-09-24 23:37:34.471165

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = "f0e06b4cdd92"
down_revision = "dc40d39de679"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chats",
        sa.Column("date", sa.DateTime, nullable=False),
        sa.Column("author_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "recipient_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column("content", JSON, nullable=False),
    )
    op.create_primary_key("pk_chats", "chats", ["author_id", "recipient_id", "date"])


def downgrade():
    op.drop_table("chats")
