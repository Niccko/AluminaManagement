"""add feed and load id

Revision ID: 433517ea3ea2
Revises: c50986f9143a
Create Date: 2023-04-01 19:11:41.880708

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '433517ea3ea2'
down_revision = 'c50986f9143a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alumina_feed', sa.Column('feed_id', sa.Integer(), nullable=False), schema='ddl')
    op.add_column('alumina_load', sa.Column('load_id', sa.Integer(), nullable=False), schema='ddl')
    op.alter_column('alumina_load', 'source_bunker_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               schema='ddl')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('alumina_load', 'source_bunker_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               schema='ddl')
    op.drop_column('alumina_load', 'load_id', schema='ddl')
    op.drop_column('alumina_feed', 'feed_id', schema='ddl')
    # ### end Alembic commands ###
