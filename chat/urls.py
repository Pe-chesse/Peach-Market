# chat/urls.py
from django.urls import path
# from chat.views import ChatIndex, ChatRoom
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_index, name='chat_index'),
    path('redis/', views.RedisMessageAPIView.as_view()),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
]