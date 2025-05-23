"""estructura

Revision ID: b5a404f6443e
Revises: f1f346b5077c
Create Date: 2025-05-07 20:05:22.890050

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b5a404f6443e"
down_revision: Union[str, None] = "f1f346b5077c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("aula", "profesor_id", existing_type=sa.Integer(), nullable=True)

    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("aula", "profesor_id", existing_type=sa.Integer(), nullable=False)

    pass
    # ### end Alembic commands ###
