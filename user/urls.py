from django.urls import path
from .views import ProtectedApiView,UserApiView

app_name = 'user'

urlpatterns = [
    path('test', ProtectedApiView.as_view()),
    path('profile', UserApiView.as_view()),
]