"""Initial migration.

Revision ID: 8720383a3ce3
Revises:
Create Date: 2021-10-04 14:27:46.797337

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8720383a3ce3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("avatar", sa.Text, nullable=True),
        sa.Column("username", sa.Unicode(100), nullable=False),
        sa.Column("fullname", sa.Unicode(255), nullable=False),
        sa.Column("email", sa.Unicode(255), nullable=False),
        sa.Column("password", sa.LargeBinary, nullable=True),
        sa.Column("valid", sa.Boolean, nullable=True),
        sa.Column("failed_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("lockout_time", sa.DateTime, nullable=True, server_default=None),
        sa.Column("salt", sa.LargeBinary, nullable=True, server_default=None),
    )

    op.create_table(
        "topics",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.Unicode(255), nullable=False),
        sa.Column("pinned", sa.Boolean, nullable=False),
        sa.Column("active", sa.Boolean, nullable=True),
        sa.Column("created", sa.DateTime, nullable=False),
        sa.Column("views", sa.Integer, nullable=False),
        sa.Column("replies", sa.Integer, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("topic_id", sa.Integer, sa.ForeignKey("topics.id"), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
    op.drop_table("topics")
    op.drop_table("users")
