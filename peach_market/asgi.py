
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peach_market.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    # "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("ws/v1/chat/", ChatConsumer.as_asgi()),
            ])
        )
    ),
})


