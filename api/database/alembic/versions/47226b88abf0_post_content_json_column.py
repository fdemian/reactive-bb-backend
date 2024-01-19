"""Post content JSON column.

Revision ID: 47226b88abf0
Revises: 65d0e1139e55
Create Date: 2022-08-20 13:41:25.533876

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = "47226b88abf0"
down_revision = "65d0e1139e55"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("posts", "content")
    op.add_column("posts", sa.Column("content", JSON, nullable=False))


def downgrade():
    op.drop_column("posts", "content")
    op.add_column("posts", sa.Column("content", sa.Text, nullable=True))
