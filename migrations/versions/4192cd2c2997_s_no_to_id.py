"""s_no to id

Revision ID: 4192cd2c2997
Revises: 
Create Date: 2024-10-27 15:49:12.244319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4192cd2c2997'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
        batch_op.alter_column('dat',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('task',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
        batch_op.drop_column('s_no')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('s_no', sa.INTEGER(), nullable=False))
        batch_op.alter_column('task',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('dat',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.drop_column('id')

    # ### end Alembic commands ###
