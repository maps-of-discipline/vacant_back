"""remomve program.priority col

Revision ID: cd1eff9711ca
Revises: b079d8a8ccf2
Create Date: 2025-03-16 23:26:34.228424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd1eff9711ca'
down_revision: Union[str, None] = 'b079d8a8ccf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('status', sa.String(), nullable=False))
    op.drop_column('program', 'priority')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('program', sa.Column('priority', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('application', 'status')
    # ### end Alembic commands ###
