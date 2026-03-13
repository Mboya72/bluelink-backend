import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import communication.routing
from communication.middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluelink.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware( # Wrap the AuthMiddlewareStack
        AuthMiddlewareStack(
            URLRouter(communication.routing.websocket_urlpatterns)
        )
    ),
})