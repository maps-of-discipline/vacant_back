"""alter user passport number field

Revision ID: 4545e7d525ed
Revises: bdeb4c8b0e05
Create Date: 2025-05-22 21:24:26.721519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4545e7d525ed'
down_revision: Union[str, None] = 'bdeb4c8b0e05'
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
