
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peach_market.settings')


django_asgi_app = get_asgi_application()

from chat.consumers import ChatConsumer
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":
        AuthMiddlewareStack(
            
            URLRouter([
                path("ws/v1/chat/", ChatConsumer.as_asgi()),
            ])
        )
})


