"""Init

Revision ID: 85b8b2bd8d9a
Revises:
Create Date: 2024-01-02 19:21:14.817480

"""
import os

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "85b8b2bd8d9a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    path = os.path.join(os.path.dirname(__file__), "..", "schema.sql")

    with open(path) as f:
        conn = op.get_bind()
        conn.execute(sa.text(f.read()))


def downgrade():
    pass
