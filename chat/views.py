import hashlib
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import ChatRoom,User,ChatMessage,ChatRoomMember
from .serializers import ChatMessageSerializer,ChatRoomMembersSerializer

def chat_room(req, room_name):
    return render(req, "chat/chat_room.html", {"room_name": room_name})


class ChatRoomAPIView(APIView):

    def post(self, request):
        try:
            def get_members(room_name):
                members = ChatRoomMember.objects.filter(chat_room = room_name)
                members_data = ChatRoomMembersSerializer(members,many = True)
                return members_data.data
            
            def get_messages(room_name):
                chat_messages = ChatMessage.objects.filter(
                chat_room=room_name
                ).order_by('-num')[:30]
                
                if chat_messages.count() == 0:
                    return []
                elif chat_messages.count() < 30:
                    limit = chat_messages.count()
                else:
                    limit = 30

                chat_messages = chat_messages[:limit][::-1]

                serializer = ChatMessageSerializer(chat_messages, many=True)
                return serializer.data

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

            
            
            return Response({
                'name':chat_room.name,
                'members':get_members(chat_room.name),
                'messages':get_messages(chat_room.name),
            },status=200)
        
        except Exception as e:
            return Response(status=400)
        

class ChatMessageListView(APIView):
    def post(self, request):
        chat_room = self.request.data.get('chat_room')
        max_num = self.request.data.get('num')
        
        try:
            chat_room = ChatRoom.objects.get(name = chat_room)
            if not chat_room.users.filter(user = request.user).count():
                return Response({'message':'권한이 없습니다'},403)

            chat_messages = ChatMessage.objects.filter(
                chat_room=chat_room,
                num__lt=max_num
            ).order_by('-num')[:30]
            
            if chat_messages.count() == 0:
                return Response({'message':'메세지를 찾을 수 없습니다.'},204)
            elif chat_messages.count() < 30:
                limit = chat_messages.count()
            else:
                limit = 30

            chat_messages = chat_messages[:limit][::-1]

            serializer = ChatMessageSerializer(chat_messages, many=True)
            return Response(serializer.data,200)
        except:
            return Response({'message':'채팅방을 찾을 수 없습니다.'},404)