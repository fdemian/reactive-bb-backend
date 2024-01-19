"""Add likes table.

Revision ID: ed0115ffeb85
Revises: 42af85d8a077
Create Date: 2021-11-26 21:01:41.568679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ed0115ffeb85"
down_revision = "42af85d8a077"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "likes",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id"), nullable=False),
    )


def downgrade():
    op.drop_table("likes")
