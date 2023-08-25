from django.urls import path
from .views import CacheMediaAPIView

app_name = 'bucket'

urlpatterns = [
    path('media/', CacheMediaAPIView.as_view()),
]