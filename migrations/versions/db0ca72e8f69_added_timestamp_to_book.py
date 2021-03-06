"""added timestamp to Book

Revision ID: db0ca72e8f69
Revises: 9331decb410b
Create Date: 2018-05-26 15:03:28.876813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db0ca72e8f69'
down_revision = '9331decb410b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('time_posted', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_book_time_posted'), 'book', ['time_posted'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_book_time_posted'), table_name='book')
    op.drop_column('book', 'time_posted')
    # ### end Alembic commands ###
