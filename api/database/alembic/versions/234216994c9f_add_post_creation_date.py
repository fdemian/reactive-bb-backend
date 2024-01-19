"""Add post creation date.

Revision ID: 234216994c9f
Revises: 3e289081bbb7
Create Date: 2021-12-09 12:55:06.751150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "234216994c9f"
down_revision = "3e289081bbb7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("created", sa.DateTime, nullable=False))


def downgrade():
    op.drop_column("posts", "created")
