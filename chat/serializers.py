from .models import ChatMessage,ChatRoom,ChatRoomMember
from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.serializers import PublicUserSerializer
User = get_user_model()

class ChatMessageSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = ChatMessage
        fields = '__all__'
    
    def get_type(self,obj):
        return 'chat.message'

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
    last_read_num = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoomMember
        fields = ['user_image_url','user_nickname','last_read_num']


    def get_user_image_url(self, obj):
        return obj.user.image_url
    
    def get_user_nickname(self, obj):
        return obj.user.nickname
    
    def get_last_read_num(self, obj):
        try:
            return obj.last_read.num
        except:
            return 0
        
class SyncMessageSerializer(serializers.ModelSerializer):

    last_message = serializers.CharField()

    class Meta:
        model = ChatRoomMember
        fields = ['chat_room','last_read','last_message']