"""Add bookmarks.

Revision ID: cec321266fe1
Revises: ed0115ffeb85
Create Date: 2021-12-01 13:36:00.898215

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "cec321266fe1"
down_revision = "ed0115ffeb85"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bookmarks",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id"), nullable=False),
    )


def downgrade():
    op.drop_table("bookmarks")
