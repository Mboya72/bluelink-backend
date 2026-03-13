from urllib.parse import parse_qs # Use this for cleaner parsing
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Decode the bytes into a string
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        
        token = query_params.get("token", [None])[0]

        if token:
            scope["user"] = await self.get_user(token)
        else:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        try:
            # This validates the token and extracts the user_id
            access_token = AccessToken(token_key)
            return User.objects.get(id=access_token["user_id"])
        except Exception:
            return AnonymousUser()