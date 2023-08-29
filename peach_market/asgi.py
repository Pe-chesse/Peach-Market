import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peach_market.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 일반 HTTP 요청을 처리하는 ASGI 핸들러
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/v1/chat/", ChatConsumer.as_asgi()),
        ])
    ),
})