"""Eliminate replies column.

Revision ID: 3e289081bbb7
Revises: cec321266fe1
Create Date: 2021-12-07 15:09:55.552096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e289081bbb7"
down_revision = "cec321266fe1"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("topics", "replies")


def downgrade():
    op.add_column("topics", sa.Column("replies", sa.Integer, nullable=True))
