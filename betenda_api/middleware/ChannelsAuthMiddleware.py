from django.db import close_old_connections
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode


class JWTAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    async def __call__(self, scope, receive, send):

        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        except:
            token = None

        # Try to authenticate the user
        if token:
            try:
                # Validate the token and raise an error if the token is invalid
                UntypedToken(token)
            except (InvalidToken, TokenError) as e:
                # Token is invalid
                print(e)
                return None
            else:
                # Then token is valid, decode it
                decoded_data = jwt_decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"])
                # Get the user
                user = await self.get_user(decoded_data["user_id"])

            return await self.inner(dict(scope, user=user), receive, send)
        return None

    @database_sync_to_async
    def get_user(self, user_id):
        return get_user_model().objects.get(id=user_id)
