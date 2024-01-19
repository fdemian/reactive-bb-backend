"""Add user validation.

Revision ID: 65d0e1139e55
Revises: 234216994c9f
Create Date: 2022-02-15 12:54:51.201154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "65d0e1139e55"
down_revision = "234216994c9f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_activation",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("token", sa.Text, nullable=False),
    )


def downgrade():
    op.drop_table("user_activation")
