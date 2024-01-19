"""Add post editing details.

Revision ID: d47b81ac12ad
Revises: 811412622c96
Create Date: 2023-02-17 14:07:52.892933

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = "d47b81ac12ad"
down_revision = "811412622c96"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts", sa.Column("edited", sa.Boolean, nullable=False, server_default="False")
    )
    op.create_table(
        "post_edits",
        sa.Column(
            "edited_post",
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
        sa.Column("previous_text", JSON, nullable=False),
        sa.Column("current_text", JSON, nullable=False),
        sa.Column("date", sa.DateTime, primary_key=True, nullable=False),
    )


def downgrade():
    op.drop_table("post_edits")
    op.drop_column("posts", "edited")
