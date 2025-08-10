from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from rest_framework_simplejwt.tokens import AccessToken  # ✅ Moved inside
        from django.contrib.auth.models import AnonymousUser

        query_string = scope['query_string'].decode()
        token = parse_qs(query_string).get("token")

        @database_sync_to_async
        def get_user(token_key):
            try:
                access_token = AccessToken(token_key)
                user_id = access_token['user_id']
                return get_user_model().objects.get(id=user_id)
            except Exception:
                return AnonymousUser()

        scope['user'] = await get_user(token[0]) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)
