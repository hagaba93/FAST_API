"""drop priority column

Revision ID: f85e902a7319
Revises: 61b47a9078a7
Create Date: 2026-01-12 00:03:34.937592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f85e902a7319'
down_revision: Union[str, Sequence[str], None] = '61b47a9078a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('todos', 'priority')
   


def downgrade() -> None:
    op.add_column('todos', sa.Column('priority', sa.Integer(), nullable=True))
    
