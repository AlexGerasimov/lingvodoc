"""Create_tables

Revision ID: 28894fa7718
Revises: 
Create Date: 2015-10-22 16:38:37.321064

"""

# revision identifiers, used by Alembic.
revision = '28894fa7718'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import lingvodoc

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('basegroup',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=True),
    sa.Column('translation_string', sa.UnicodeText(), nullable=True),
    sa.Column('subject', sa.UnicodeText(), nullable=True),
    sa.Column('action', sa.UnicodeText(), nullable=True),
    sa.Column('dictionary_default', sa.Boolean(), nullable=True),
    sa.Column('perspective_default', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('language',
    sa.Column('object_id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('translation_string', sa.UnicodeText(), nullable=True),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['language.object_id', 'language.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('organization',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=True),
    sa.Column('about', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('uitranslationstring',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('locale_id', sa.BigInteger(), nullable=True),
    sa.Column('translation_string', sa.UnicodeText(), nullable=True),
    sa.Column('translation', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userentitiestranslationstring',
    sa.Column('object_id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('locale_id', sa.BigInteger(), nullable=True),
    sa.Column('translation_string', sa.UnicodeText(), nullable=True),
    sa.Column('translation', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('dictionary',
    sa.Column('object_id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('state', sa.UnicodeText(), nullable=True),
    sa.Column('authors', sa.UnicodeText(), nullable=True),
    sa.Column('translation_string', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['language.object_id', 'language.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('group',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('base_group_id', lingvodoc.models.SLBigInteger(), nullable=True),
    sa.Column('subject_client_id', sa.BigInteger(), nullable=True),
    sa.Column('subject_object_id', sa.BigInteger(), nullable=True),
    sa.Column('subject_override', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['base_group_id'], ['basegroup.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locale',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('shortcut', sa.UnicodeText(), nullable=True),
    sa.Column('intl_name', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['language.object_id', 'language.client_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dictionaryperspective',
    sa.Column('object_id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('state', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('translation_string', sa.UnicodeText(), nullable=True),
    sa.Column('is_template', sa.Boolean(), nullable=True),
    sa.Column('import_source', sa.UnicodeText(), nullable=True),
    sa.Column('import_hash', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['dictionary.object_id', 'dictionary.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('organization_to_group_association',
    sa.Column('organization_id', sa.BigInteger(), nullable=True),
    sa.Column('group_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], )
    )
    op.create_table('user',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('login', sa.UnicodeText(), nullable=True),
    sa.Column('name', sa.UnicodeText(), nullable=True),
    sa.Column('intl_name', sa.UnicodeText(), nullable=True),
    sa.Column('default_locale_id', lingvodoc.models.SLBigInteger(), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('signup_date', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['default_locale_id'], ['locale.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('about',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('locale_id', lingvodoc.models.SLBigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['locale_id'], ['locale.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_id')
    )
    op.create_table('client',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('counter', sa.BigInteger(), nullable=True),
    sa.Column('creation_time', sa.DateTime(), nullable=True),
    sa.Column('is_browser_client', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dictionaryperspectivefield',
    sa.Column('object_id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_object_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_type', sa.UnicodeText(), nullable=True),
    sa.Column('data_type', sa.UnicodeText(), nullable=True),
    sa.Column('level', sa.UnicodeText(), nullable=True),
    sa.Column('group', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('state', sa.UnicodeText(), nullable=True),
    sa.Column('position', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['entity_object_id', 'entity_client_id'], ['dictionaryperspectivefield.object_id', 'dictionaryperspectivefield.client_id'], ),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['dictionaryperspective.object_id', 'dictionaryperspective.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('email',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('email', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('lexicalentry',
    sa.Column('object_id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('moved_to', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('additional_metadata', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['dictionaryperspective.object_id', 'dictionaryperspective.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('passhash',
    sa.Column('id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('hash', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_to_dictionary_association',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('dictionary_client_id', sa.BigInteger(), nullable=True),
    sa.Column('dictionary_object_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['dictionary_client_id', 'dictionary_object_id'], ['dictionary.client_id', 'dictionary.object_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_to_group_association',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('group_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_to_organization_association',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('organization_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('userblobs',
    sa.Column('object_id', lingvodoc.models.SLBigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('real_storage_path', sa.UnicodeText(), nullable=True),
    sa.Column('data_type', sa.UnicodeText(), nullable=True),
    sa.Column('additional_metadata', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('groupingentity',
    sa.Column('object_id', sa.BigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_type', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('additional_metadata', sa.UnicodeText(), nullable=True),
    sa.Column('is_translatable', sa.Boolean(), nullable=True),
    sa.Column('locale_id', sa.BigInteger(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('tag', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['lexicalentry.object_id', 'lexicalentry.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('leveloneentity',
    sa.Column('object_id', sa.BigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_type', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('additional_metadata', sa.UnicodeText(), nullable=True),
    sa.Column('is_translatable', sa.Boolean(), nullable=True),
    sa.Column('locale_id', sa.BigInteger(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['lexicalentry.object_id', 'lexicalentry.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('leveltwoentity',
    sa.Column('object_id', sa.BigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_type', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('additional_metadata', sa.UnicodeText(), nullable=True),
    sa.Column('is_translatable', sa.Boolean(), nullable=True),
    sa.Column('locale_id', sa.BigInteger(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['leveloneentity.object_id', 'leveloneentity.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('publishgroupingentity',
    sa.Column('object_id', sa.BigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_object_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_type', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['entity_object_id', 'entity_client_id'], ['groupingentity.object_id', 'groupingentity.client_id'], ),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['lexicalentry.object_id', 'lexicalentry.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('publishleveloneentity',
    sa.Column('object_id', sa.BigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_object_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_type', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['entity_object_id', 'entity_client_id'], ['leveloneentity.object_id', 'leveloneentity.client_id'], ),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['lexicalentry.object_id', 'lexicalentry.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    op.create_table('publishleveltwoentity',
    sa.Column('object_id', sa.BigInteger(), nullable=False),
    sa.Column('client_id', sa.BigInteger(), nullable=False),
    sa.Column('parent_object_id', sa.BigInteger(), nullable=True),
    sa.Column('parent_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_object_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_client_id', sa.BigInteger(), nullable=True),
    sa.Column('entity_type', sa.UnicodeText(), nullable=True),
    sa.Column('content', sa.UnicodeText(), nullable=True),
    sa.Column('marked_for_deletion', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['entity_object_id', 'entity_client_id'], ['leveltwoentity.object_id', 'leveltwoentity.client_id'], ),
    sa.ForeignKeyConstraint(['parent_object_id', 'parent_client_id'], ['lexicalentry.object_id', 'lexicalentry.client_id'], ),
    sa.PrimaryKeyConstraint('object_id', 'client_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publishleveltwoentity')
    op.drop_table('publishleveloneentity')
    op.drop_table('publishgroupingentity')
    op.drop_table('leveltwoentity')
    op.drop_table('leveloneentity')
    op.drop_table('groupingentity')
    op.drop_table('userblobs')
    op.drop_table('user_to_organization_association')
    op.drop_table('user_to_group_association')
    op.drop_table('user_to_dictionary_association')
    op.drop_table('passhash')
    op.drop_table('lexicalentry')
    op.drop_table('email')
    op.drop_table('dictionaryperspectivefield')
    op.drop_table('client')
    op.drop_table('about')
    op.drop_table('user')
    op.drop_table('organization_to_group_association')
    op.drop_table('dictionaryperspective')
    op.drop_table('locale')
    op.drop_table('group')
    op.drop_table('dictionary')
    op.drop_table('userentitiestranslationstring')
    op.drop_table('uitranslationstring')
    op.drop_table('organization')
    op.drop_table('language')
    op.drop_table('basegroup')
    ### end Alembic commands ###
