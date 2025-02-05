"""empty message

Revision ID: 45bbc5b2c935
Revises: a76c88b21e0f
Create Date: 2022-07-07 15:55:10.464113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45bbc5b2c935'
down_revision = 'a76c88b21e0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('art_show',
    sa.Column('art_id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['art_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['show_id'], ['shows.id'], ),
    sa.PrimaryKeyConstraint('art_id', 'show_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('art_show')
    # ### end Alembic commands ###
