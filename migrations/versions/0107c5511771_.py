"""empty message

Revision ID: 0107c5511771
Revises: c0c6bf974034
Create Date: 2022-07-08 16:20:51.885597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0107c5511771'
down_revision = 'c0c6bf974034'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('genre', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genre')
    # ### end Alembic commands ###
