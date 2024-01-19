"""Add categories.

Revision ID: fc4e1997563f
Revises: 8720383a3ce3
Create Date: 2021-10-15 19:19:34.309174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fc4e1997563f"
down_revision = "8720383a3ce3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.Unicode(255), nullable=False),
        sa.Column("description", sa.Unicode(255), nullable=False),
    )
    op.add_column(
        "topics",
        sa.Column(
            "category_id", sa.Integer, sa.ForeignKey("categories.id"), nullable=True
        ),
    )


def downgrade():
    op.drop_column("topics", "category_id")
    op.drop_table("categories")
