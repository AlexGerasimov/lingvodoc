import graphene

from lingvodoc.schema.gql_entity import (
    Entity,
    CreateEntity,
    UpdateEntity,
    DeleteEntity
)
from lingvodoc.schema.gql_dictipersptofield import (
    DictionaryPerspectiveToField,
    CreateDictionaryPerspectiveToField,
    UpdateDictionaryPerspectiveToField,
    DeleteDictionaryPerspectiveToField
)
from lingvodoc.schema.gql_basegroup import (
    BaseGroup,
)
from lingvodoc.schema.gql_group import (
    Group
)
from lingvodoc.schema.gql_organization import (
    Organization,
    CreateOrganization,
    UpdateOrganization,
    DeleteOrganization
)
from lingvodoc.schema.gql_publishingentity import (
    PublishingEntity
)
from lingvodoc.schema.gql_translationatom import (
    TranslationAtom,
    CreateTranslationAtom,
    UpdateTranslationAtom
)
from lingvodoc.schema.gql_translationgist import (
    TranslationGist,
    CreateTranslationGist,
    DeleteTranslationGist
)
from lingvodoc.schema.gql_userblobs import (
    UserBlobs
)
from lingvodoc.schema.gql_field import (
    Field,
    CreateField,
    UpdateField,
    DeleteField
)

from lingvodoc.schema.gql_dictionary import (
    Dictionary,
    CreateDictionary,
    UpdateDictionary,
    DeleteDictionary
)

from lingvodoc.schema.gql_lexicalentry import (
    LexicalEntry,
    CreateLexicalEntry,
    DeleteLexicalEntry
)

from lingvodoc.schema.gql_language import (
    Language,
    CreateLanguage,
    UpdateLanguage,
    DeleteLanguage
)
from lingvodoc.schema.gql_dictionaryperspective import (
    DictionaryPerspective,
    CreateDictionaryPerspective,
    UpdateDictionaryPerspective,
    DeleteDictionaryPerspective
)
from lingvodoc.schema.gql_user import (
    User,
    CreateUser,
    UpdateUser
)
from lingvodoc.schema.gql_grant import (
    Grant,
    CreateGrant,
    UpdateGrant,
    DeleteGrant
)
from lingvodoc.schema.gql_email import (
    Email
)
from lingvodoc.schema.gql_holders import PermissionException

import lingvodoc.acl as acl

from lingvodoc.models import (
    DBSession,
    Dictionary as dbDictionary,
    DictionaryPerspective as dbPerspective,
    Language as dbLanguage,
    Organization as dbOrganization,
    TranslationAtom as dbTranslationAtom,
    UserBlobs as dbUserBlobs,
    Client
)
from pyramid.request import Request

from sqlalchemy import (
    and_,
    or_,
    tuple_
)

from sqlalchemy.orm import aliased

from sqlalchemy.sql.functions import coalesce

from pyramid.security import authenticated_userid

RUSSIAN_LOCALE = 1
ENGLISH_LOCALE = 2


class Query(graphene.ObjectType):
    client = graphene.String()
    dictionaries = graphene.List(Dictionary, published=graphene.Boolean())
    dictionary = graphene.Field(Dictionary, id=graphene.List(graphene.Int))
    perspectives = graphene.List(DictionaryPerspective, published=graphene.Boolean())
    perspective = graphene.Field(DictionaryPerspective, id=graphene.List(graphene.Int))
    entity = graphene.Field(Entity, id=graphene.List(graphene.Int))
    language = graphene.Field(Language, id=graphene.List(graphene.Int))
    languages = graphene.List(Language)
    user = graphene.Field(User, id=graphene.Int())
    field = graphene.Field(Field, id=graphene.List(graphene.Int))
    translationatom = graphene.Field(TranslationAtom, id=graphene.List(graphene.Int))
    translationgist = graphene.Field(TranslationGist, id=graphene.List(graphene.Int))
    organization = graphene.Field(Organization, id=graphene.List(graphene.Int))
    organizations = graphene.List(Organization)


    def resolve_dictionaries(self, info, published):
        """
        example:

        query DictionaryList {
            dictionaries(published: true) {
                id
                translation
                parent_id
                translation_gist_id
                state_translation_gist_id
                category
                domain
            }
        }
        """
        context = info.context
        dbdicts = list()
        request = context.get('request')
        if published:

            subreq = Request.blank('/translation_service_search')
            subreq.method = 'POST'
            subreq.headers = request.headers
            subreq.json = {'searchstring': 'Published'}
            headers = dict()
            if request.headers.get('Cookie'):
                headers = {'Cookie': request.headers['Cookie']}
            subreq.headers = headers
            resp = request.invoke_subrequest(subreq)

            if 'error' not in resp.json:
                state_translation_gist_object_id, state_translation_gist_client_id = resp.json['object_id'], resp.json[
                    'client_id']
            else:
                raise KeyError("Something wrong with the base", resp.json['error'])

            subreq = Request.blank('/translation_service_search')
            subreq.method = 'POST'
            subreq.headers = request.headers
            subreq.json = {'searchstring': 'Limited access'}  # todo: fix
            headers = dict()
            if request.headers.get('Cookie'):
                headers = {'Cookie': request.headers['Cookie']}
            subreq.headers = headers
            resp = request.invoke_subrequest(subreq)

            if 'error' not in resp.json:
                limited_object_id, limited_client_id = resp.json['object_id'], resp.json['client_id']
            else:
                raise KeyError("Something wrong with the base", resp.json['error'])

            dbdicts = DBSession.query(dbDictionary).filter(
                or_(and_(dbDictionary.state_translation_gist_object_id == state_translation_gist_object_id,
                         dbDictionary.state_translation_gist_client_id == state_translation_gist_client_id),
                    and_(dbDictionary.state_translation_gist_object_id == limited_object_id,
                         dbDictionary.state_translation_gist_client_id == limited_client_id))). \
                join(dbPerspective) \
                .filter(or_(and_(dbPerspective.state_translation_gist_object_id == state_translation_gist_object_id,
                                 dbPerspective.state_translation_gist_client_id == state_translation_gist_client_id),
                            and_(dbPerspective.state_translation_gist_object_id == limited_object_id,
                                 dbPerspective.state_translation_gist_client_id == limited_client_id))). \
                filter(dbPerspective.marked_for_deletion == False).all()

        else:
            dbdicts = DBSession.query(dbDictionary).filter(dbPerspective.marked_for_deletion == False).all()

        dictionaries_list = [Dictionary(id=[dbdict.client_id, dbdict.object_id],
                                        parent_id=[dbdict.parent_client_id, dbdict.parent_object_id],
                                        translation_gist_id=[dbdict.translation_gist_client_id, dbdict.translation_gist_object_id],
                                        state_translation_gist_id=[dbdict.state_translation_gist_client_id, dbdict.state_translation_gist_object_id],
                                        category=dbdict.category,
                                        domain=dbdict.domain,
                                        translation=dbdict.get_translation(context.get('locale_id'))) for dbdict in dbdicts]
        return dictionaries_list

    def resolve_dictionary(self, info, id):
        return Dictionary(id=id)

    def resolve_perspectives(self,info, published):
        """
        example:

        query LanguagesList {
            perspectives(published: true) {
                id
                translation
                parent_id
                translation_gist_id
                state_translation_gist_id
                import_source
                import_hash
            }
        }
        """
        context = info.context
        request = context.get('request')
        if published:
            subreq = Request.blank('/translation_service_search')
            subreq.method = 'POST'
            subreq.headers = request.headers
            subreq.json = {'searchstring': 'Published'}
            headers = {'Cookie': request.headers['Cookie']}
            subreq.headers = headers
            resp = request.invoke_subrequest(subreq)
            if 'error' not in resp.json:
                state_translation_gist_object_id, state_translation_gist_client_id = resp.json['object_id'], resp.json[
                    'client_id']
            else:
                raise KeyError("Something wrong with the base", resp.json['error'])

            subreq = Request.blank('/translation_service_search')
            subreq.method = 'POST'
            subreq.headers = request.headers
            subreq.json = {'searchstring': 'Limited access'}
            headers = {'Cookie': request.headers['Cookie']}
            subreq.headers = headers
            resp = request.invoke_subrequest(subreq)
            if 'error' not in resp.json:
                limited_object_id, limited_client_id = resp.json['object_id'], resp.json[
                    'client_id']
            else:
                raise KeyError("Something wrong with the base", resp.json['error'])

            """
            atom_perspective_name_alias = aliased(dbTranslationAtom, name="PerspectiveName")
            atom_perspective_name_fallback_alias = aliased(dbTranslationAtom, name="PerspectiveNameFallback")
            persps = DBSession.query(dbPerspective,
                                     dbTranslationAtom,
                                     coalesce(atom_perspective_name_alias.content,
                                              atom_perspective_name_fallback_alias.content,
                                              "No translation for your locale available").label("Translation")
                                     ).filter(dbPerspective.marked_for_deletion == False)
            """
            persps = DBSession.query(dbPerspective).filter(
                or_(and_(dbPerspective.state_translation_gist_object_id == state_translation_gist_object_id,
                         dbPerspective.state_translation_gist_client_id == state_translation_gist_client_id),
                    and_(dbPerspective.state_translation_gist_object_id == limited_object_id,
                         dbDictionary.state_translation_gist_client_id == limited_client_id))). \
                filter(dbPerspective.marked_for_deletion == False).all()
        else:
            persps = DBSession.query(dbPerspective).filter(dbPerspective.marked_for_deletion == False).all()

        perspectives_list = [DictionaryPerspective(id=[persp.client_id, persp.object_id],
                                                   parent_id=[persp.parent_client_id, persp.parent_object_id],
                                                   translation_gist_id=[persp.translation_gist_client_id, persp.translation_gist_object_id],
                                                   state_translation_gist_id=[persp.state_translation_gist_client_id, persp.state_translation_gist_object_id],
                                                   import_source=persp.import_source, import_hash=persp.import_hash,
                                                   translation=persp.get_translation(context.get('locale_id'))) for persp in persps]
        return perspectives_list


    def resolve_perspective(self, info, id):
        return DictionaryPerspective(id=id)

    def resolve_language(self, info, id):
        return Language(id=id)

    def resolve_languages(self, info):
        """
        example:

        query LanguagesList {
            languages {
                id
                translation
                parent_id
                translation_gist_id
            }
        }
        """
        context = info.context

        languages = DBSession.query(dbLanguage).filter(dbLanguage.marked_for_deletion == False).all()
        languages_list = [Language(id=[lang.client_id, lang.object_id],
                                   parent_id=[lang.parent_client_id, lang.parent_object_id],
                                   translation_gist_id=[lang.translation_gist_client_id, lang.translation_gist_object_id],
                                   translation=lang.get_translation(context.get('locale_id'))) for lang in languages]
        return languages_list

    def resolve_entity(self, info, id):
        return Entity(id=id)

    def resolve_user(self, info, id):
        return User(id=id)

    # def resolve_datetime(self, args, context, info):
    #     id = args.get('id')
    #     return DateTime(id=id)

    def resolve_basegroup(self, info, id):
        return BaseGroup(id=id)

    def resolve_client(self, info):
        context = info.context
        return context.get('client')

    def resolve_dictionaryperspectivetofield(self, info, id):
        return DictionaryPerspectiveToField(id=id)

    def resolve_email(self, info, id):
        return Email(id=id)

    def resolve_grant(self, info, id):
        return Grant(id=id)

    def resolve_group(self, info, id):
        return Group(id=id)

    def resolve_organization(self, info, id):
        return Organization(id=id)

    def resolve_organizations(self, info):
        organizations = DBSession.query(dbOrganization).filter_by(marked_for_deletion=False).all()
        organizations_list = [Organization(name=organization.name,
                                           about=organization.about) for organization in organizations]
        return organizations_list

    # def resolve_passhash(self, args, context, info):
    #     id = args.get('id')
    #     return Passhash(id=id)

    # def resolve_objecttoc(self, args, context, info):
    #     id = args.get('id')
    #     return ObjectTOC(id=id)

    def resolve_publishingentity(self, info, id):
        return PublishingEntity(id=id)

    def resolve_translationatom(self, info, id):
        return TranslationAtom(id=id)

    def resolve_translationgist(self, info, id):
        return TranslationGist(id=id)

    def resolve_userblobs(self, info, id):
        return UserBlobs(id=id)

    def resolve_field(self, info, id):
        client_id = info.context.get("client_id")
        return Field(id=id)

    def resolve_lexicalentry(self, info, id):
        return LexicalEntry(id=id)


class MyMutations(graphene.ObjectType):
    """
    Mutation classes.
    It may be replaced by
    create_field = gql_field.CreateField.Field()
    for more beautiful imports
    """
    create_field = CreateField.Field()
    update_field = UpdateField.Field()
    delete_field = DeleteField.Field()
    create_entity = CreateEntity.Field()
    update_entity = UpdateEntity.Field()
    delete_entity = DeleteEntity.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_language = CreateLanguage.Field()
    update_language = UpdateLanguage.Field()
    delete_language = DeleteLanguage.Field()
    create_dictionary = CreateDictionary.Field()
    update_dictionary = UpdateDictionary.Field()
    delete_dictionary = DeleteDictionary.Field()
    create_organization = CreateOrganization.Field()
    update_organization = UpdateOrganization.Field()
    delete_organization = DeleteOrganization.Field()
    create_translationatom = CreateTranslationAtom.Field()
    update_translationatom = UpdateTranslationAtom.Field()
    create_translationgist = CreateTranslationGist.Field()
    delete_translationgist = DeleteTranslationGist.Field()
    create_lexicalentry = CreateLexicalEntry.Field()
    delete_lexicalentry = DeleteLexicalEntry.Field()
    create_perspective = CreateDictionaryPerspective.Field()
    update_perspective = UpdateDictionaryPerspective.Field()
    delete_perspective = DeleteDictionaryPerspective.Field()
    create_perspective_to_field = CreateDictionaryPerspectiveToField.Field()
    update_perspective_to_field = UpdateDictionaryPerspectiveToField.Field()
    delete_perspective_to_field = DeleteDictionaryPerspectiveToField.Field()
    create_grant = CreateGrant.Field()
    update_grant = UpdateGrant.Field()
    delete_grant = DeleteGrant.Field()

schema = graphene.Schema(query=Query, auto_camelcase=False, mutation=MyMutations)

class Context(dict):
    """
    Context for graphene query execution, works as dict for arbitrary key-value associations and supports
    ACL-based permission checking.
    """

    def __init__(self, context_dict):
        """
        Initializes query execution context by initializing context key-value dictionary and, hopefully,
        getting client id and request data.
        """

        dict.__init__(self, context_dict)

        self.client_id = context_dict.get('client_id')
        self.request = context_dict.get('request')

        self.cache = {}

    def acl_check_if(self, action, subject, subject_id):
        """
        Checks if the client has permission to perform given action on a specified subject via ACL.
        """
        if type(subject_id) is list:
            subject_id = tuple(subject_id)

        if (action, subject, subject_id) in self.cache:
            return self.cache[(action, subject, subject_id)]

        result = acl.check_direct(self.client_id, self.request, action, subject, subject_id)
        self.cache[(action, subject, subject_id)] = result

        return result

    def acl_check(self, action, subject, subject_id):
        """
        Checks if the client has permission to perform given action on a specified subject via ACL, raises
        permission exception otherwise.
        """

        if not self.acl_check_if(action, subject, subject_id):
            raise PermissionException(self.client_id, action, subject, subject_id)

    def acl_check_with_id_if(self, action, subject, args):
        """
        Checks via ACL if the client has permission to perform given action on a specified subject, with
        subject identifier extracted from query execution arguments.
        """

        return self.acl_check_if(action, subject, args.get('id'))