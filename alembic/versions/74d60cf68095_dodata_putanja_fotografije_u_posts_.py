"""Dodata putanja_fotografije u posts tabelu

Revision ID: 74d60cf68095
Revises: fdaf41ba7b20
Create Date: 2024-11-18 15:23:33.687561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74d60cf68095'
down_revision: Union[str, None] = 'fdaf41ba7b20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
