"""empty message

Revision ID: daf000b3eeed
Revises: ef253b2e8816
Create Date: 2023-08-23 19:23:46.486369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daf000b3eeed'
down_revision = 'ef253b2e8816'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.drop_constraint('teams_pokemon_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'pokemon', ['pokemon_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('teams_pokemon_id_fkey', 'user', ['pokemon_id'], ['id'])

    # ### end Alembic commands ###
