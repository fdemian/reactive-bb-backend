"""Add flagged posts table.

Revision ID: 811412622c96
Revises: 62204a79bc6e
Create Date: 2023-02-04 17:48:47.982983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "811412622c96"
down_revision = "62204a79bc6e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "flagged_posts",
        sa.Column(
            "post_id",
            sa.Integer,
            sa.ForeignKey("posts.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("reason_id", sa.Integer, nullable=False),
        sa.Column("reason_text", sa.Text, nullable=True),
    )


def downgrade():
    op.drop_table("flagged_posts")
