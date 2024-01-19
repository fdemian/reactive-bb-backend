"""Add password reset models.

Revision ID: b5621f79d104
Revises: d47b81ac12ad
Create Date: 2023-04-04 00:06:30.056184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b5621f79d104"
down_revision = "d47b81ac12ad"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "password_reset",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id"),
            primary_key=False,
            nullable=False,
        ),
        sa.Column("token", sa.Text, primary_key=True, nullable=False),
        sa.Column("expires", sa.DateTime, primary_key=False, nullable=False),
    )


def downgrade():
    op.drop_table("password_reset")
