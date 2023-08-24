import hashlib
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import ChatRoom,User
from user.firebase import FirebaseAuthentication


def chat_room(req, room_name):
    return render(req, "chat/chat_room.html", {"room_name": room_name})


class ChatRoomAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            target_nickname = request.data.get('nickname')
            target_user = User.objects.get(nickname = target_nickname)
            format_room = sorted([target_user,request.user],key=lambda x:x.pk)
            
            hash_object = hashlib.md5()
            hash_object.update(' '.join([i.username for i in format_room]).encode())
            room_name = hash_object.hexdigest()[:32]

            try:
                chat_room = ChatRoom.objects.get(name = room_name)
            except:
                chat_room = ChatRoom.objects.create(name = room_name)
                chat_room.users.set(format_room)
            
            return Response(chat_room.name,status=200)
        
        except Exception as e:
            return Response(status=400)
