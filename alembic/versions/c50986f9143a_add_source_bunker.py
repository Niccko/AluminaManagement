"""add source_bunker

Revision ID: c50986f9143a
Revises: 313663926ca4
Create Date: 2023-03-24 23:28:05.497881

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'c50986f9143a'
down_revision = '313663926ca4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alumina_load',
    sa.Column('load_dt', sa.DateTime(timezone=True), nullable=False),
    sa.Column('bunker_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('source_bunker_id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bunker_id'], ['ddl.bunker.bunker_id'], ),
    sa.ForeignKeyConstraint(['process_id'], ['ddl.process.process_id'], ),
    sa.ForeignKeyConstraint(['source_bunker_id'], ['ddl.bunker.bunker_id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['ddl.alumina_type.type_id'], ),
    sa.PrimaryKeyConstraint('load_dt', 'bunker_id', 'type_id'),
    schema='ddl'
    )


def downgrade() -> None:
    op.drop_table('alumina_load', schema='ddl')

    # ### end Alembic commands ###
