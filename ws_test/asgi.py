"""
ASGI config for ws_test project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.testings.routing 
from channels.auth import AuthMiddlewareStack
from .middleware import JWTAuthMiddleware
import django

django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ws_test.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddleware(URLRouter(apps.testings.routing.testings_urlpatterns))
}
)
