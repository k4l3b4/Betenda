import os

from django.core.asgi import get_asgi_application
from betenda_api.middleware.ChannelsAuthMiddleware import JWTAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from betenda_api.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betenda_api.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
