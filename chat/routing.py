from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/v1/chat/", consumers.ChatConsumer.as_asgi()),
]