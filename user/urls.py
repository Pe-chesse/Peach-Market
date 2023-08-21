from django.urls import path
from .views import ProtectedApiView,UserApiView, FollowAPIView

app_name = 'user'

urlpatterns = [
    path('test', ProtectedApiView.as_view()),
    path('profile', UserApiView.as_view()),
    path('follow/<int:user_id>/',FollowAPIView.as_view()),
]