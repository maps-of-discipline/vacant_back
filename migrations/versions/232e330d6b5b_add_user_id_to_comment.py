"""add user_id to comment

Revision ID: 232e330d6b5b
Revises: 06466066ec65
Create Date: 2025-04-23 01:53:10.778661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '232e330d6b5b'
down_revision: Union[str, None] = '06466066ec65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('user_id', sa.String(), nullable=False))
    op.create_foreign_key(None, 'comment', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'user_id')
    # ### end Alembic commands ###
