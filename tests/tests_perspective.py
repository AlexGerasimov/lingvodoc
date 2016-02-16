from tests.tests import MyTestCase

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPOk,
    HTTPBadRequest,
    HTTPConflict,
    HTTPInternalServerError,
    HTTPUnauthorized,
    HTTPFound,
    HTTPForbidden
)

class PerspectiveTest(MyTestCase):
    def _build_ordered_lists(self, response, correct_answer):
        self.assertEqual(response.status_int, HTTPOk.code)
        answer = sorted(correct_answer, key=lambda x: (x['client_id'], x['object_id']))
        response = response.json
        result = list()
        for i in response['perspectives']:
            self.assertIn('client_id', i)
            self.assertIn('object_id', i)
            result.append(dict(client_id = i['client_id'], object_id = i['object_id']))
        result = sorted(result, key=lambda x: (x['client_id'], x['object_id']))
        return (result, answer)

    def _perspective_role_assertion(self, response, correct_answer):
        self.assertIn('roles_users', response.json)
        self.assertEqual(sorted(response.json['roles_users'].items()),
                         sorted(correct_answer['roles_users'].items()))
        self.assertIn('roles_organizations', response.json)
        self.assertEqual(sorted(response.json['roles_organizations'].items()),
                         sorted(correct_answer['roles_organizations'].items()))

    def testAllPerspectives(self):
        id_tester = self.signup_common()
        id_u1 = self.signup_common('user1', 'user1')
        id_l1 = self.create_language('language1')
        dict_1 = self.create_dictionary('user1_dict1', id_l1)
        default_persp = [
            {"object_id": 1, "client_id": 1},
            {"object_id": 2, "client_id": 1},
            {"object_id": 3, "client_id": 1}
        ]

        response = self.app.get('/perspectives',
                                params = {'is_template': False})
        result, answer = self._build_ordered_lists(response, [])
        self.assertFalse(result)

        persp_1 = self.create_perspective('translation_string1', dict_1, "Published", False)
        persp_2 = self.create_perspective('translation_string2', dict_1, "Published", True)
        persp_3 = self.create_perspective('translation_string3', dict_1, "Marked", False)
        persp_4 = self.create_perspective('translation_string4', dict_1, "Marked", True)

        response = self.app.get('/perspectives',
                                params = {'is_template': True})
        result, answer = self._build_ordered_lists(response, default_persp + [persp_2, persp_4])
        self.assertEqual(result, answer)

        response = self.app.get('/perspectives',
                                params = {'is_template': False})
        result, answer = self._build_ordered_lists(response, [persp_1, persp_3])
        self.assertEqual(result, answer)

        response = self.app.get('/perspectives',
                                params = {'state': "Published"})
        result, answer = self._build_ordered_lists(response, [persp_1, persp_2])
        self.assertEqual(result, answer)

        response = self.app.get('/perspectives',
                                params = {'state': "Marked", 'is_template': False})
        result, answer = self._build_ordered_lists(response, [persp_3])
        self.assertEqual(result, answer)

        response = self.app.get('/perspectives',
                                params = {'state': "NoState"})
        result, answer = self._build_ordered_lists(response, [])
        self.assertFalse(result)

        response = self.app.get('/perspectives')
        result, answer = self._build_ordered_lists(
            response, default_persp + [persp_1, persp_2, persp_3, persp_4])
        self.assertEqual(result, answer)

    def testPerspectives(self):
        id_tester = self.signup_common()
        id_u1 = self.signup_common('user1', 'user1')
        id_l1 = self.create_language('language1')
        dict_1 = self.create_dictionary('user1_dict1', id_l1)
        dict_2 = self.create_dictionary('user1_dict2', id_l1)
        unexisting_dict = {"object_id": 4, "client_id": 4}
        persp_1 = self.create_perspective('translation_string1', dict_1, "Published", False)
        persp_2 = self.create_perspective('translation_string1', dict_1, "Marked", True)

        response = self.app.get('/dictionary/%(client_id)s/%(object_id)s/perspectives' % dict_1)
        result, answer = self._build_ordered_lists(response, [persp_1, persp_2])
        self.assertEqual(result, answer)

        response = self.app.get('/dictionary/%(client_id)s/%(object_id)s/perspectives' % dict_2)
        result, answer = self._build_ordered_lists(response, [])
        self.assertFalse(result)

        #TODO: catch bad response exception and check it
        # try:
        #     response = self.app.get('/dictionary/%(client_id)s/%(object_id)s/perspectives' % unexisting_dict)
        # except AppError as app_error:
        #
        # self.assertEqual(response.status_int, HTTPNotFound.code)

    def testViewPerspectiveRoles(self):
        id_tester = self.signup_common()
        id_u1 = self.signup_common('user1', 'user1')
        id_u2 = self.signup_common('user2', 'user1')
        id_u3 = self.signup_common('user3', 'user1')
        id_l1 = self.create_language('language1')
        dict_1 = self.create_dictionary('user1_dict1', id_l1)
        persp_1 = self.create_perspective('translation_string1', dict_1, "Published", False)

        correct_answer = {
            'roles_users': {
                "Can view published lexical entries": [id_u1, id_u2],
                "Can get perspective role list": [id_u1],
                "Can view unpublished lexical entries": [id_u1, id_u2],
                "Can create perspective roles and assign collaborators": [id_u1, id_u2, id_u3],
                "Can approve lexical entries and publish": [id_u1, id_u3],
                "Can resign users from dictionary editors": [id_u1, id_u2],
                "Can create lexical entries": [id_u1],
                "Can edit perspective": [id_u1, id_u2],
                "Can deactivate lexical entries": [id_u1, id_u2],
                "Can delete lexical entries": [id_u1, id_u2],
                "Can delete perspective": [id_u1, id_u2]
            },
            "roles_organizations": {
                "Can view published lexical entries": [],
                "Can get perspective role list": [],
                "Can view unpublished lexical entries": [],
                "Can create perspective roles and assign collaborators": [],
                "Can approve lexical entries and publish": [],
                "Can resign users from dictionary editors": [],
                "Can create lexical entries": [],
                "Can edit perspective": [],
                "Can deactivate lexical entries": [],
                "Can delete lexical entries": [],
                "Can delete perspective": []
            }
        }
        params = {'roles_users':
                              {"Can create lexical entries": [],
                               "Can get perspective role list": [id_u1],
                               "Can resign users from dictionary editors": [id_u2],
                               "Can approve lexical entries and publish": [id_u3],
                               "Can create perspective roles and assign collaborators":[id_u2, id_u3],
                               "Can edit perspective": [id_u2],
                               "Can delete perspective": [id_u2],
                               "Can delete lexical entries": [id_u2],
                               "Can deactivate lexical entries": [id_u2],
                               "Can view unpublished lexical entries": [id_u2],
                               "Can view published lexical entries": [id_u2]}
                  }

        # Testing get and post
        response = self.app.post_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        # Add single role permission
        params = {'roles_users':
                              {"Can view unpublished lexical entries": [id_u3]}}
        correct_answer['roles_users']['Can view unpublished lexical entries'] += [id_u3]
        response = self.app.post_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        # Empty tests
        params = {'roles_users': {}}
        response = self.app.post_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        params = {}
        response = self.app.post_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        # Testing get and delete
        # Delete one user
        params = {'roles_users':
                              {"Can view unpublished lexical entries": [id_u3]}}
        correct_answer['roles_users']['Can view unpublished lexical entries'] = [id_u1, id_u2]
        response = self.app.delete_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        # Delete user that is not presented in the list
        params = {'roles_users':
                              {"Can resign users from dictionary editors": [id_u3]}}
        response = self.app.delete_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        # Delete several users
        params = {'roles_users':
                              {"Can create perspective roles and assign collaborators": [id_u2, id_u3]}}
        correct_answer['roles_users']['Can create perspective roles and assign collaborators'] = [id_u1]
        response = self.app.delete_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        # Empty tests
        params = {'roles_users':
                              {}}
        response = self.app.delete_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        params = {}
        response = self.app.delete_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self._perspective_role_assertion(response, correct_answer)

        # TODO: add test for prohibited deletion of the owner from user roles

    def testPerspectiveInfo(self):
        id_tester = self.signup_common()
        id_u1 = self.signup_common('user1', 'user1')
        id_u2 = self.signup_common('user2', 'user1')
        id_u3 = self.signup_common('user3', 'user1')
        id_l1 = self.create_language('language1')
        dict_1 = self.create_dictionary('user1_dict1', id_l1)
        persp_1 = self.create_perspective('translation_string1', dict_1, "Published", False)

        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/fields'
                                % (1, 1, 1, 1))
        self.assertEqual(response.status_int, HTTPOk.code)
        fields = response.json
        response = self.app.post_json('/dictionary/%s/%s/perspective/%s/%s/fields'
                                      % (dict_1['client_id'],
                                         dict_1['object_id'],
                                         persp_1['client_id'],
                                         persp_1['object_id']),
                                      params=fields)
        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/info' %
                                (dict_1['client_id'], dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        self.assertDictEqual(response.json, {"count": []})

        params = {'roles_users':
                              {"Can create lexical entries": [id_u1, id_u2],
                               "Can get perspective role list": [id_u1, id_u2],
                               "Can resign users from dictionary editors": [id_u1, id_u2],
                               "Can approve lexical entries and publish": [id_u1, id_u2],
                               "Can create perspective roles and assign collaborators":[id_u1, id_u2],
                               "Can edit perspective": [id_u1, id_u2],
                               "Can delete perspective": [id_u1, id_u2],
                               "Can delete lexical entries": [id_u1, id_u2],
                               "Can deactivate lexical entries": [id_u1, id_u2],
                               "Can view unpublished lexical entries": [id_u1, id_u2],
                               "Can view published lexical entries": [id_u1, id_u2]}
                  }
        response = self.app.post_json('/dictionary/%s/%s/perspective/%s/%s/roles' % (dict_1['client_id'],
                                   dict_1['object_id'], persp_1['client_id'], persp_1['object_id']), params=params)

        response = self.app.post_json('/dictionary/%s/%s/perspective/%s/%s/lexical_entries' %
                              (dict_1['client_id'], dict_1['object_id'],
                               persp_1['client_id'], persp_1['object_id']), params={'count': 3})
        to_be_approved = list()
        to_be_approved.append(self.add_l1e(dict_1, persp_1, response.json[0], 'text1', 'Word'))
        to_be_approved.append(self.add_l1e(dict_1, persp_1, response.json[0], 'text2', 'Word'))
        to_be_approved.append(self.add_l1e(dict_1, persp_1, response.json[0], 'translation1', 'Translation'))
        to_be_approved.append(self.add_l1e(dict_1, persp_1, response.json[1], 'translation2', 'Translation'))
        self.login_common(username='user2')
        # We don't want to approve this entity
        self.add_l1e(dict_1, persp_1, response.json[1], 'text3', 'Word')
        to_be_approved.append(self.add_l1e(dict_1, persp_1, response.json[1], 'translation3', 'Translation'))
        to_be_approved.append(self.add_l1e(dict_1, persp_1, response.json[2], 'transcription1', 'Transcription'))
        list(map(lambda x: x.update({"type": 'leveloneentity'}), to_be_approved))

        response = self.app.patch_json(
            '/dictionary/%s/%s/perspective/%s/%s/approve' % (dict_1['client_id'], dict_1['object_id'],
                                                             persp_1['client_id'], persp_1['object_id']),
            params={"entities": to_be_approved}
        )

        response = self.app.get('/dictionary/%s/%s/perspective/%s/%s/info' %
                                (dict_1['client_id'], dict_1['object_id'], persp_1['client_id'], persp_1['object_id']))
        correct_answer = {
            "count": [
                {
                "login": "user1",
                "intl_name": "user1",
                "counters": {
                    "Transcription": 0,
                    "Sound": 0,
                    "Translation": 2,
                    "Paradigm transcription": 0,
                    "lexical_entry": 3,
                    "Paradigm translation": 0,
                    "Etymology": 0,
                    "Paradigm sound": 0,
                    "Word": 2,
                    "Paradigm word": 0,
                    "Paradigm Praat markup": 0,
                    "Praat markup": 0
                },
                "name": "test",
                "id": 3
            }, {
                "login": "user2",
                "intl_name": "user2",
                "counters": {
                    "Transcription": 1,
                    "Sound": 0,
                    "Translation": 1,
                    "Paradigm transcription": 0,
                    "lexical_entry": 0,
                    "Paradigm translation": 0,
                    "Etymology": 0,
                    "Paradigm sound": 0,
                    "Word": 0,
                    "Paradigm word": 0,
                    "Paradigm Praat markup": 0,
                    "Praat markup": 0
                },
                "name": "test",
                "id": 4
            }]
        }
        self.assertDictEqual(response.json, correct_answer)