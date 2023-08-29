from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import consumers

application = ProtocolTypeRouter({
    # HTTP protocol (normal Django views)
    "http": get_asgi_application(),

    # WebSocket protocol (Channels consumers)
    "websocket": URLRouter([
        path("ws/v1/chat/", consumers.ChatConsumer.as_asgi()),
        path("ws/some_path/", consumers.SomeConsumer.as_asgi()),
        # Add more paths and consumers as needed
    ]),
})
