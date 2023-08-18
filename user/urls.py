from django.urls import path
from .views import ProtectedApiView

app_name = 'user'

urlpatterns = [
    path('test', ProtectedApiView.as_view()),
]