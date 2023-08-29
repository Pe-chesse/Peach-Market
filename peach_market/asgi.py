import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peach_market.settings')

django.setup()

application = get_asgi_application()