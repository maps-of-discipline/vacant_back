"""alter user.pass_data col

Revision ID: b079d8a8ccf2
Revises: 11c8f6b3c9e1
Create Date: 2025-03-13 00:04:38.826042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b079d8a8ccf2'
down_revision: Union[str, None] = '11c8f6b3c9e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'passport_data',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'passport_data',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
