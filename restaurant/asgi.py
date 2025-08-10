"""
ASGI config for restaurant project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter , URLRouter 


import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')
django.setup()

from django.core.asgi import get_asgi_application
from middleware.TokenAuthMiddleware import JWTAuthMiddleware 
import api.routing
import orders.routing
import reports.routing


django_asgi_app = get_asgi_application()

websocket_patterns = api.routing.websocket_urlpatterns + orders.routing.websocket_urlpatterns + reports.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_patterns)
    )
})
