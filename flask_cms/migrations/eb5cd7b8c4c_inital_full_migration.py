"""inital full migration

Revision ID: eb5cd7b8c4c
Revises: None
Create Date: 2014-10-27 17:44:34.984694

"""

# revision identifiers, used by Alembic.
revision = 'eb5cd7b8c4c'
down_revision = None
from uuid import uuid4 

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('template_blocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('block_id')
    )
    op.create_table('static_blocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('block_id', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('block_id')
    )
    op.create_table('font_icon_librarys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('call_string', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('call_string'),
    sa.UniqueConstraint('name')
    )
    op.create_table('admin_tabs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('tab_id', sa.String(length=50), nullable=False),
    sa.Column('tab_title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('ip_address', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('macros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('_args', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('base_template', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('can_view', sa.Boolean(), nullable=False),
    sa.Column('can_add', sa.Boolean(), nullable=False),
    sa.Column('can_edit', sa.Boolean(), nullable=False),
    sa.Column('can_delete', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('directories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('full_path', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_path')
    )
    op.create_table('types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('html', sa.Text(), nullable=True),
    sa.Column('field_type', sa.String(length=255), nullable=True),
    sa.Column('required', sa.Boolean(), nullable=True),
    sa.Column('data_type', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('font_icons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('library_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['library_id'], ['font_icon_librarys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('setting_type_id', sa.Integer(), nullable=True),
    sa.Column('default', sa.String(length=255), nullable=True),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['setting_type_id'], ['types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('widgets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('add_date', sa.DateTime(), nullable=True),
    sa.Column('_pw_hash', sa.UnicodeText(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('icon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['icon_id'], ['font_icons.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('icon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['icon_id'], ['font_icons.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=True),
    sa.Column('visits', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('buttons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('color', sa.Enum('blue', 'grey', 'light-blue', 'yellow', 'green', 'red',name="color_enum_{}".format(uuid4().hex)), nullable=False),
    sa.Column('size', sa.Enum('XL', 'L', 'M', 'S', 'XS',name="size_enum_{}".format(uuid4().hex)), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('icon', sa.String(length=255), nullable=True),
    sa.Column('icon_library', sa.String(length=255), nullable=True),
    sa.Column('_endpoint', sa.String(length=255), nullable=True),
    sa.Column('is_link', sa.Boolean(), nullable=True),
    sa.Column('icon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['icon_id'], ['font_icons.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('pages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('add_to_nav', sa.Boolean(), nullable=True),
    sa.Column('add_left_sidebar', sa.Boolean(), nullable=True),
    sa.Column('add_right_sidebar', sa.Boolean(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.Column('meta_title', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('short_url', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('icon_id', sa.Integer(), nullable=True),
   sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['icon_id'], ['font_icons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pages_template_blocks',
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.Column('template_block_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], ),
    sa.ForeignKeyConstraint(['template_block_id'], ['template_blocks.id'], )
    )
    op.create_table('pages_macros',
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.Column('macro_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['macro_id'], ['macros.id'], ),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], )
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('meta_title', sa.String(length=255), nullable=True),
    sa.Column('tags', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('excerpt_length', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=True),
    sa.Column('icon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['icon_id'], ['font_icons.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('articles')
    op.drop_table('pages_macros')
    op.drop_table('pages_template_blocks')
    op.drop_table('blogs')
    op.drop_table('pages')
    op.drop_table('buttons')
    op.drop_table('profiles')
    op.drop_table('categories')
    op.drop_table('tags')
    op.drop_table('users')
    op.drop_table('widgets')
    op.drop_table('settings')
    op.drop_table('font_icons')
    op.drop_table('types')
    op.drop_table('directories')
    op.drop_table('roles')
    op.drop_table('templates')
    op.drop_table('macros')
    op.drop_table('blocks')
    op.drop_table('contact_messages')
    op.drop_table('admin_tabs')
    op.drop_table('font_icon_librarys')
    op.drop_table('static_blocks')
    op.drop_table('template_blocks')
    ### end Alembic commands ###
