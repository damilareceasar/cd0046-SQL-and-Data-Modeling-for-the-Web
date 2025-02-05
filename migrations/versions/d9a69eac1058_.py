"""empty message

Revision ID: d9a69eac1058
Revises: 30548114047d
Create Date: 2022-07-05 17:36:21.260513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9a69eac1058'
down_revision = '30548114047d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Venue_relId_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'relId')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('relId', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Venue_relId_fkey', 'Venue', 'Artist', ['relId'], ['id'])
    # ### end Alembic commands ###
