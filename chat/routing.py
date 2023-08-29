from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/v1/chat/$', consumers.ChatConsumer.as_asgi()),
    # Add more websocket URL patterns if needed
]