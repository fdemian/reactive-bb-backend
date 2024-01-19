"""Add ban expiration field.

Revision ID: 62204a79bc6e
Revises: 35857e77badf
Create Date: 2023-02-02 22:07:42.769440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62204a79bc6e"
down_revision = "35857e77badf"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("ban_expires", sa.DateTime, nullable=True))


def downgrade():
    op.drop_column("users", "ban_expires")
