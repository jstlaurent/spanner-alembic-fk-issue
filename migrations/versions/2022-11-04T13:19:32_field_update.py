

"""field_update

Revision ID: 0a924cea0163
Revises: 974b951041b0
Create Date: 2022-11-04 13:19:32.075608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a924cea0163'
down_revision = '974b951041b0'
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        # ### commands auto generated by Alembic - please adjust! ###
        with op.batch_alter_table('a', schema=None) as batch_op:
            batch_op.add_column(sa.Column('content', sa.String(), nullable=False))

        with op.batch_alter_table('link', schema=None) as batch_op:
            batch_op.drop_constraint('fk_1', type_='foreignkey')
            batch_op.drop_constraint('fk_2', type_='foreignkey')
            batch_op.create_foreign_key('fk_1', 'a', ['environment_id', 'a_id'], ['environment_id', 'id'])
            batch_op.create_foreign_key('fk_2', 'b', ['environment_id', 'b_id'], ['environment_id', 'id'])

        # ### end Alembic commands ###


def downgrade():
    with op.get_context().autocommit_block():
        # ### commands auto generated by Alembic - please adjust! ###
        with op.batch_alter_table('link', schema=None) as batch_op:
            batch_op.drop_constraint('fk_2', type_='foreignkey')
            batch_op.drop_constraint('fk_1', type_='foreignkey')
            batch_op.create_foreign_key('fk_2', 'b', ['environment_id', 'b_id'], ['id', 'environment_id'])
            batch_op.create_foreign_key('fk_1', 'a', ['environment_id', 'a_id'], ['id', 'environment_id'])

        with op.batch_alter_table('a', schema=None) as batch_op:
            batch_op.drop_column('content')

        # ### end Alembic commands ###
