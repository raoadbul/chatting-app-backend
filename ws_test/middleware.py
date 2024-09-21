from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.conf import settings
from urllib.parse import parse_qs


User = get_user_model()

@database_sync_to_async
def get_user(token_key):
    try:
        token = AccessToken(token_key)
        user_id = token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        return None

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token_key = query_string.get("token")
        print('xxxxxxxxx')
        if token_key:
            user = await get_user(token_key[0])
            if user:
                scope['user'] = user

        await super().__call__(scope, receive, send)