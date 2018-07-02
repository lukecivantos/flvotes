"""empty message

Revision ID: 527e8f16751e
Revises: 879fe8a73df4
Create Date: 2018-06-25 16:54:45.603261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '527e8f16751e'
down_revision = '879fe8a73df4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registrants', sa.Column('ref', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('registrants', 'ref')
    # ### end Alembic commands ###