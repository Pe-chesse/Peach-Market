from django.urls import path
from .views import ProtectedApiView,UserApiView, FollowView

app_name = 'user'

urlpatterns = [
    path('test', ProtectedApiView.as_view()),
    path('profile', UserApiView.as_view()),
    path('<int:user_id>/follow/',FollowView.as_view()),
]