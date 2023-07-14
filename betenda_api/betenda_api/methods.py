from enum import Enum
import random
import string
from django.utils import timezone
from Users.models import Invitation, User
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class UnAuthenticated(APIException):
    """
    Requesting client is not a user
    """

    def __init__(self, message):
        self.detail = message


class PermissionDenied(APIException):
    """
    User doesn't have permission to perform an action
    """

    def __init__(self, message):
        self.detail = message


class ResourceNotFound(APIException):
    """
    Requested data is not found
    """

    def __init__(self, message):
        self.detail = message


class BadRequest(APIException):
    """
    Data that is sent over is not correct
    """

    def __init__(self, message):
        self.detail = message


class UselessRequest(APIException):
    """
    The request to the API is useless, ie trying to verify an email after it has already been verified
    """

    def __init__(self, message):
        self.detail = message


class VersionError(APIException):
    """
    API version in the request is not valid
    """

    def __init__(self, message):
        self.detail = message


class PaymentRequired(APIException):
    """
    The user i.e the school owner is behind on payments
    """

    def __init__(self, message):
        self.detail = message


class ServerError(APIException):
    """
    There is a server error
    """

    def __init__(self, message):
        self.detail = message


class UnknownError(APIException):
    """
    There is a server error
    """

    def __init__(self, message):
        self.detail = message


def send_response(data: str | dict, msg: str, code: int = 200):
    """
    takes a data(string or dict), msg(string) and code(int) to send a JsonResponse with the format of:\n
    {
        "data": data,\n
        "message": "msg"
    }
    """
    return Response({"data": data, "message": msg, "timestamp": timezone.now()}, status=code)


class ErrorType(Enum):
    """
    VERSION_ERROR = When the API version in the request is not valid \n
    PERMISSION_DENIED = When the user doesn't have permission to perform an action \n
    UNAUTHENTICATED = When the requesting client is not a user \n
    BAD_REQUEST = When the data that is sent over is not correct \n
    METHOD_NOT_ALLOWED = When the requested data is not found \n
    NOT_FOUND = When the requested data is not found \n
    USELESS_REQUEST = When a request to the API is useless, ie trying to verify an email after it has already been verified \n 
    SERVER_ERROR = When there is a server error \n
    PAYMENT_REQUIRED = When the user i.e the school owner is behind on payments \n
    UNKNOWN_ERROR = When there is an error that doesn't have a known type \n
    """
    VERSION_ERROR = 'Version_Error'
    """
    When the api version in the request is not valid
    """
    PERMISSION_DENIED = 'Permission_Denied'
    """
    When the user doesn't have permission to perform an action
    """
    UNAUTHENTICATED = 'Unauthenticated'
    """
    When the requesting client is not a user
    """
    UNAUTHORIZED = 'Unauthorized'
    """
    When the user isn't within a certain group of user
    """
    BAD_REQUEST = 'Bad_Request'
    """
    When the data that is sent over is not correct
    """
    METHOD_NOT_ALLOWED = 'Method_Not_Allowed'
    """
    When the data that is sent over is not correct
    """
    NOT_FOUND = 'Resource_Not_Found'
    """
    When the requested data is not found
    """
    USELESS_REQUEST = 'Useless_Request'
    """
    When a request to the api is useless, ie trying to verify an email after it has already been verified
    """
    SERVER_ERROR = 'Server_Error'
    """
    When there is a server error
    """
    PAYMENT_REQUIRED = 'Payment_Required'
    """
    When the user i.e the school owner is behind on payments
    """
    UNKNOWN_ERROR = 'Unknown_Error'
    """
    When there is an error that doesn't have a known type
    """


def send_error(err_type: ErrorType, err: str | dict, code: int = 400):
    """
    takes an err_type(ErrorType["VERSION_ERROR", "PERMISSION_ERROR", "UNAUTHENTICATED", "UNAUTHORIZED", "BAD_REQUEST", "USELESS_REQUEST", "SERVER_ERROR", "PAYMENT_REQUIRED", "UNKNOWN_ERROR",
    ]), err(string or dict) and code(int) to send a JsonResponse Error with the format of:\n
    {
        "type": err_type,\n
        "error": err
    }
    """
    return Response({"type": err_type.value, "error": err, "timestamp": timezone.now()}, status=code)


def check_api_version(request, version, *args, **kwargs):
    if not request.version:
        raise BadRequest("Please include an API version in your request")
    elif request.version != version:
        return False
    else:
        return True


# def check_user_permissions(user, perms=None, check_all_perms=False, groups=None):
#     """
#     Takes a user object, a perms list, an all_perms bool (to determine if the user should have all the perms),
#     and an optional groups list (to check if the user is in the specified groups).
#     Returns True if the user has the required permissions (and belongs to the specified groups if provided),
#     otherwise returns False.
#     """
#     # if group is not None but the user isn't in the group(s) return False
#     if groups and not user.groups.filter(name__in=groups).exists():
#         return False
#     # if
#     if not perms:
#         return True
#     if check_all_perms:
#         return user.has_perms(perms)
#     return any(user.has_perm(perm) for perm in perms)


def check_user_permissions(user, perms=None, check_all_perms=False, groups=None):
    """
    Takes a user object, an optional perms list, an all_perms bool (to determine if the user should have all the perms),
    and an optional groups list (to check if the user is in the specified groups). \n
    Note: if both groups and perms are passed the 'or' operator is used to check if the user is either in the groups or has the perm(s) \n
    Returns True if the user has the required permissions and belongs to the specified groups (if provided),
    or if no permissions or groups are specified. Returns False otherwise.
    """
    if perms and groups:
        if check_all_perms:
            if user.has_perms(perms) or user.groups.filter(name__in=groups).exists():
                return True
        else:
            if any(user.has_perm(perm) for perm in perms) or user.groups.filter(name__in=groups).exists():
                return True
    elif perms:
        if check_all_perms:
            if user.has_perms(perms):
                return True
        else:
            if any(user.has_perm(perm) for perm in perms):
                return True
    elif groups:
        if user.groups.filter(name__in=groups).exists():
            return True
    else:
        return True

    return False
