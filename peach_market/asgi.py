
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path
import firebase_admin
from peach_market.settings import env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peach_market.settings')


django_asgi_app = get_asgi_application()


if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate(env('FIREBASE_KEY_PATH'))
    firebase_admin.initialize_app(cred)

from chat.consumers import ChatConsumer
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        re_path(r"ws/v1/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    ])
})


