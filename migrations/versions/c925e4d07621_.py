"""empty message

Revision ID: c925e4d07621
Revises: d5059cfd2e07
Create Date: 2018-08-13 16:14:34.242246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c925e4d07621'
down_revision = 'd5059cfd2e07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registrants', sa.Column('dob_year', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('registrants', 'dob_year')
    # ### end Alembic commands ###