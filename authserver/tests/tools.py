import logging
from django.db import connections
# from django_nose.tools import *
from django.test.utils import override_settings
from nose.tools import raises, timed
from rest_framework.test import APITransactionTestCase, APIClient


class JSONAPIClient(APIClient):
    """ Set default content_type of GET request to json """
    def get(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        if not content_type:
            content_type = 'application/json'

        response = self.generic('GET', path, data, content_type, **extra)

        if follow:
            response = self._handle_redirects(response, **extra)

        return response

    def request(self, **kwargs):
        # Ensure that any credentials set get added to every request.
        kwargs.update({'wsgi.url_scheme': 'https'})
        return super(JSONAPIClient, self).request(**kwargs)


class JSONAPITransactionTestCase(APITransactionTestCase):
    client_class = JSONAPIClient


logger = logging.getLogger(__name__)

REQUIRED_HEADERS = [
    'etag',
    'content-type',

    # Django secure
    # 'x-xss-protection',
    # 'x-content-type-options',
    # 'x-frame-options',
    # 'strict-transport-security',
]

OPTIONAL_HEADERS = [
    'vary', 'pragma', 'cache-control', 'allow',
    'access-control-allow-origin'
]

# I prefer plurals
assert_list_equals = assert_list_equal


def assert_length(collection, length, msg=None):
    assert_equal(len(collection), length, msg)


def assert_is_not_blank(obj):
    assert_is_not_none(obj)
    assert_not_equals(obj, u'')


def assert_is_blank(obj):
    assert_equals(obj, u'')


def assert_keys_equals(dictionary, keys):
    assert_list_equals(
        sorted(dictionary.keys()),
        sorted(keys)
    )


def assert_is_blank_file(thing):
    from django.core.files.base import File
    assert_is_instance(thing, File)
    assert_false(thing)  # Empty File bools to False


def assert_is_string(thing):
    assert_is_instance(thing, basestring)


def assert_count(query, count):
    assert_equals(query.count(), count)


def assert_jok(response, message=None, status_code=200):
    """ Assert that a response has the expected (JSON) headers
    and the status code is ok """

    logger.info(response)

    assert_code(response, status_code)
    response_headers = response._headers

    assert_equals(
        response_headers['content-type'],
        ('Content-Type', 'application/json'),
        'Response is not JSON'
    )

    for header in REQUIRED_HEADERS:
        assert_true(
            header in response_headers,
            'Response is missing header {}'.format(header)
        )

    for header in response_headers:
        assert_true(
            header in REQUIRED_HEADERS or header in OPTIONAL_HEADERS,
            'Response has unexpected header: {}'.format(header)
        )

    assert_true(hasattr(response, 'data'), 'Response has no data')


def assert_error(response, status_code=400, **kwargs):
    assert_jok(response, status_code=status_code)
    assert_equals(
        response.data,
        kwargs
    )


def assert_error_auth(response):
    assert_error(
        response,
        403,
        detail="Authentication credentials were not provided.",
        error='NotAuthenticated'
    )


def assert_error_no_permission(response):
    assert_error(
        response,
        403,
        detail="You do not have permission to perform this action.",
        error='PermissionDenied'
    )


def assert_error_method_not_allowed(response, method='GET'):
    assert_error(
        response,
        405,
        detail="Method '{}' not allowed.".format(method),
        error='MethodNotAllowed'
    )


def assert_error_not_found(response):
    assert_error(
        response,
        404,
        detail="Not found",
    )


def assert_error_inactive(response):
    assert_error(
        response,
        403,
        detail='User is inactive',
        error='UserInactiveError'
    )


def get_db_queries():
    return connections['default'].queries


def assert_between(num, min, max):
    assert_true(
        min <= num <= max,
        '{} is not in the range {} to {}'.format(num, min, max)
    )
