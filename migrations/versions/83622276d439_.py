"""empty message

Revision ID: 83622276d439
Revises:
Create Date: 2018-05-23 17:58:47.616987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83622276d439'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('license',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('backgroundColor', sa.String(length=6), nullable=False),
    sa.Column('textColor', sa.String(length=6), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('reset_password_token', sa.String(length=100), server_default='', nullable=False),
    sa.Column('rank', sa.Enum('NOT_JOINED', 'NEW_MEMBER', 'MEMBER', 'EDITOR', 'MODERATOR', 'ADMIN', name='userrank'), nullable=True),
    sa.Column('github_username', sa.String(length=50), nullable=True),
    sa.Column('forums_username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('display_name', sa.String(length=100), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('forums_username'),
    sa.UniqueConstraint('github_username'),
    sa.UniqueConstraint('username')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('causer_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['causer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('package',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('shortDesc', sa.String(length=200), nullable=False),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('type', sa.Enum('MOD', 'GAME', 'TXP', name='packagetype'), nullable=True),
    sa.Column('license_id', sa.Integer(), nullable=True),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.Column('repo', sa.String(length=200), nullable=True),
    sa.Column('website', sa.String(length=200), nullable=True),
    sa.Column('issueTracker', sa.String(length=200), nullable=True),
    sa.Column('forums', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['license_id'], ['license.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_email_verification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('edit_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.String(length=1000), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('harddeps',
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.Column('dependency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dependency_id'], ['package.id'], ),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('package_id', 'dependency_id')
    )
    op.create_table('package_release',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('releaseDate', sa.DateTime(), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.Column('task_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('package_screenshot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('softdeps',
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.Column('dependency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dependency_id'], ['package.id'], ),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.PrimaryKeyConstraint('package_id', 'dependency_id')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['package_id'], ['package.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'package_id')
    )
    op.create_table('edit_request_change',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.Column('key', sa.Enum('name', 'title', 'shortDesc', 'desc', 'type', 'license', 'tags', 'repo', 'website', 'issueTracker', 'forums', name='packagepropertykey'), nullable=False),
    sa.Column('oldValue', sa.Text(), nullable=True),
    sa.Column('newValue', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['edit_request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('edit_request_change')
    op.drop_table('tags')
    op.drop_table('softdeps')
    op.drop_table('package_screenshot')
    op.drop_table('package_release')
    op.drop_table('harddeps')
    op.drop_table('edit_request')
    op.drop_table('user_email_verification')
    op.drop_table('package')
    op.drop_table('notification')
    op.drop_table('user')
    op.drop_table('tag')
    op.drop_table('license')
    # ### end Alembic commands ###
