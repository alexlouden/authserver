import logging

from .tools import (
    JSONAPITransactionTestCase,
    assert_equals, assert_keys_equals,
    assert_is_not_blank, assert_length,
    assert_jok, assert_code, assert_true,
    assert_is_blank_file, assert_num_queries,
    raises, get_db_queries,
    assert_error_method_not_allowed
)

from eternaleve.models import User
from eternaleve.serializers import UserSerializer

logger = logging.getLogger(__name__)


class TestUser(JSONAPITransactionTestCase):

    def test_create_user(self):

        alex = User.objects.create_user('Alex', 'alex@louden.com')

        assert_equals(alex.name, 'Alex')
        assert_equals(alex.email, 'alex@louden.com')
        assert_equals(alex.is_active, True)
        assert_equals(alex.is_admin, False)
        assert_equals(alex.is_staff, False)
        assert_equals(alex.picture, '')


class TestUserSerialiser(JSONAPITransactionTestCase):

    EXPECTED_KEYS = [
        'id',
        'name',
        'picture',
        'is_friend'
    ]

    def test_user(self):

        alex = User.objects.create_user('Alex', 'alex@louden.com')

        data = UserSerializer(alex).data

        # {'id': 2, 'name': u'Alex', 'picture': u'', 'is_friend': False}
        assert_equals(data['id'], alex.id)
        assert_equals(data['name'], alex.name)
        assert_equals(data['picture'], alex.picture)
        assert_equals(data['is_friend'], False)

        assert_keys_equals(data, self.EXPECTED_KEYS)
