import redis
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
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


class RedisMessageAPIView(APIView):
    def get(self, request):
        redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        messages = redis_instance.lrange('chat_bf64ea2189bd928a', 0, -1)
        print(messages)
        return Response({'messages': messages})
