from django.urls import path
from .views import ProtectedApiView,UserApiView, FollowAPIView,NicknameVerifyApiView

app_name = 'user'

urlpatterns = [
    path('verify/', ProtectedApiView.as_view()),
    path('profile/', UserApiView.as_view()),
    path('follow/<str:nickname>/',FollowAPIView.as_view()),
    path('nickname/',NicknameVerifyApiView.as_view()),
]