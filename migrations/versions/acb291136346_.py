"""empty message

Revision ID: acb291136346
Revises: 13a9cbe9544e
Create Date: 2022-07-05 19:32:11.242922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acb291136346'
down_revision = '13a9cbe9544e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('relId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'venue', 'artist', ['relId'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'venue', type_='foreignkey')
    op.drop_column('venue', 'relId')
    # ### end Alembic commands ###
