from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        auth = JWTAuthentication()

        if "query_string" in scope:
            query_string = scope["query_string"].decode()
            validated_token = await self.get_validated_token(auth, query_string)
            user = await self.get_user(auth, validated_token)

            if user.is_authenticated:
                scope["user"] = user

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_validated_token(self, auth, query_string):
        try:
            token = query_string.split("=")[1]
            return auth.get_validated_token(token)
        except:
            return None

    @database_sync_to_async
    def get_user(self, auth, validated_token):
        try:
            return auth.get_user(validated_token)
        except:
            return AnonymousUser()