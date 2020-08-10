"""empty message

Revision ID: 403d63f8b623
Revises: 
Create Date: 2020-08-08 01:49:21.024181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '403d63f8b623'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('github_access_token', sa.String(length=255), nullable=True),
    sa.Column('github_id', sa.Integer(), nullable=True),
    sa.Column('github_login', sa.String(length=255), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
