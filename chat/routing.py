from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/v1/chat/$', ChatConsumer.as_asgi()),
    # Add more websocket URL patterns if needed
]