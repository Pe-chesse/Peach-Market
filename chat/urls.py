# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('room/', views.ChatRoomAPIView.as_view()),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
]