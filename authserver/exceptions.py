from rest_framework.exceptions import *


class UserInactiveError(PermissionDenied):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'User is inactive'


class UserDeletedError(PermissionDenied):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'User is deleted'
