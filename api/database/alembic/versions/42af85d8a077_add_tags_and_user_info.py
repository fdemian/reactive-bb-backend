"""Add tags and user info.

Revision ID: 42af85d8a077
Revises: fc4e1997563f
Create Date: 2021-10-18 17:13:38.131315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "42af85d8a077"
down_revision = "fc4e1997563f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("topics", sa.Column("tags", sa.Text, nullable=True))
    op.add_column("users", sa.Column("status", sa.Text, nullable=True))
    op.add_column("users", sa.Column("about", sa.Text, nullable=True))


def downgrade():
    op.drop_column("topics", "tags")
    op.drop_column("users", "status")
    op.drop_column("users", "about")
