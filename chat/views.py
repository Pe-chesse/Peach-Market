from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django.views import View


def chat_index(req):
    return render(req, "chat/chat_index.html")

def chat_room(req, room_name):
    return render(req, "chat/chat_room.html", {"room_name": room_name})

# class ChatIndex(View):
#     def get(self, req):
#         return render(req, "chat/chat_index.html")

# class ChatRoom(View):
#     def get(self, req, room_name):
#         return render(req, "chat/chat_room.html", {"room_name": room_name})
