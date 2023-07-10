from rest_framework.exceptions import MethodNotAllowed, NotAuthenticated
from lesan_api.methods import ActionNotAllowed, BadRequest, ErrorType, PaymentRequired, PermissionDenied, ResourceNotFound, ServerError, UnAuthenticated, UselessRequest, VersionError, send_error
from rest_framework.views import exception_handler

def lesan_exception_handler(exc:str | dict, context):
    if isinstance(exc, PermissionDenied):
        return send_error(err_type=ErrorType.PERMISSION_ERROR, err=exc.detail, code=403)
    elif isinstance(exc, ActionNotAllowed):
        return send_error(err_type=ErrorType.UNAUTHORIZED, err=exc.detail, code=403)
    elif isinstance(exc, UnAuthenticated):
        return send_error(err_type=ErrorType.UNAUTHENTICATED, err=exc.detail, code=401)
    elif isinstance(exc, NotAuthenticated):
        return send_error(err_type=ErrorType.UNAUTHENTICATED, err=exc.detail, code=401)
    elif isinstance(exc, BadRequest):
        return send_error(err_type=ErrorType.BAD_REQUEST, err=exc.detail, code=400)
    elif isinstance(exc, ResourceNotFound):
        return send_error(err_type=ErrorType.NOT_FOUND, err=exc.detail, code=404)
    elif isinstance(exc, UselessRequest):
        return send_error(err_type=ErrorType.USELESS_REQUEST, err=exc.detail, code=403)
    elif isinstance(exc, VersionError):
        return send_error(err_type=ErrorType.VERSION_ERROR, err=exc.detail, code=400)
    elif isinstance(exc, PaymentRequired):
        return send_error(err_type=ErrorType.PAYMENT_REQUIRED, err=exc.detail, code=403)
    elif isinstance(exc, MethodNotAllowed):
        return send_error(err_type=ErrorType.METHOD_NOT_ALLOWED, err=exc.detail, code=405)
    # elif isinstance(exc, Http404):
    #     return send_error(err_type=ErrorType.NOT_FOUND, err=exc.detail, code=404)
    elif isinstance(exc, ServerError):
        return send_error(err_type=ErrorType.SERVER_ERROR, err=exc.detail, code=500)
    return exception_handler(exc, context)
