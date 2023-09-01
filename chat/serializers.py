from .models import ChatMessage,ChatRoom,ChatRoomMember
from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.serializers import PublicUserSerializer

User = get_user_model()

class ChatMessageSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['type','num','chat_room','content','status','user','time']
    
    def get_type(self, obj):
        return 'chat.message'
    
    def get_user(self, obj):
        serializer = PublicUserSerializer(obj.sender)
        return serializer.data

class SummaryMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['num','content']

class ChatRoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['name','user_list','last_message']
        
    def get_user_list(self, obj):
        serializer = PublicUserSerializer(obj.users, many=True)
        return serializer.data
    
    def get_last_message(self, obj):
        try:
            last_message = ChatMessage.objects.filter(chat_room = obj.name).last
            return last_message.content
        except:
            return ''
        
class ChatRoomMembersSerializer(serializers.ModelSerializer):
    user_image_url = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    user_email= serializers.SerializerMethodField()
    last_read_num = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoomMember
        fields = ['user_image_url','user_nickname','user_email','last_read_num']

    def get_user_image_url(self, obj):
        try:
            return obj.user.image_url.profile_image.name
        except:
            return None
    
    def get_user_email(self, obj):
        return obj.user.email
    
    def get_user_nickname(self, obj):
        return obj.user.nickname
    
    def get_last_read_num(self, obj):
        try:
            return obj.last_read.num
        except:
            return 0
        
class SyncMessageSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    last_read = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoomMember
        fields = ['chat_room','last_read','last_message']

    def get_last_message(self, obj):
        chat_room = ChatRoom.objects.get(name = obj.chat_room)
        if chat_room.last_message:
            serializer = SummaryMessageSerializer(chat_room.last_message)
            return serializer.data
        return 0
    
    def get_last_read(self, obj):
        return obj.last_read.num if obj.last_read else 0