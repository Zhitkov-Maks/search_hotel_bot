"""add colomn distance

Revision ID: 218e07eb5602
Revises: 4f250c2875c1
Create Date: 2023-11-24 20:18:43.377328

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "218e07eb5602"
down_revision: Union[str, None] = "4f250c2875c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("hotels", sa.Column("distance", sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("hotels", "distance")
    # ### end Alembic commands ###