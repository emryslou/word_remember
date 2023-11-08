"""v1

Revision ID: aebbd3824bbf
Revises: c40f1d19717d
Create Date: 2023-03-31 16:08:15.615180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aebbd3824bbf'
down_revision = 'c40f1d19717d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('word_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(), nullable=True),
    sa.Column('dict_link', sa.String(), nullable=True),
    sa.Column('voice', sa.String(), nullable=True),
    sa.Column('type_zh', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_word_list_id'), 'word_list', ['id'], unique=False)
    op.create_index(op.f('ix_word_list_word'), 'word_list', ['word'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_word_list_word'), table_name='word_list')
    op.drop_index(op.f('ix_word_list_id'), table_name='word_list')
    op.drop_table('word_list')
    # ### end Alembic commands ###
