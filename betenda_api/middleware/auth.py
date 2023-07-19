from rest_framework import HTTP_HEADER_ENCODING, authentication
from django.contrib.auth import get_user_model


class JWTAuthenticationCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        return self.get_response(request)

    # def __init__(self, get_response):
    #     self.get_response = get_response

    # def __call__(self, request):
    #     jwt_auth = JWTAuthentication()

    #     token = request.COOKIES.get('access')

    #     if token:
    #         request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    #         user = jwt_auth.authenticate(request)

    #         if user:
    #             request.user = user

    #     return self.get_response(request)


class JWTAuthentication(authentication.BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    token provided in a request header.
    """

    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request):
        cookie = request.COOKIES.get("access")
        if cookie:
            raw_token = cookie.encode(HTTP_HEADER_ENCODING)
            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        return None
