import json, redis
from channels.generic.websocket import  AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import SyncToAsync
from .models import ChatRoom,ChatMessage,ChatRoomMember
from .serializers import ChatMessageSerializer,ChatRoomMembersSerializer,SyncMessageSerializer


class ChatConsumer(AsyncWebsocketConsumer): # async
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    async def connect(self):
        self.room_group_name = f"base_{self.scope['user'].username}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.get_sync_message()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        message_data = json.loads(text_data)
        match message_data.get('type'):
            case 'send_chat':
                await self.receive_chat(message_data)
            case 'active_chat':
                await self.active_chat(message_data)
            case 'deactive_chat':
                await self.deactive_chat(message_data)

    async def chat_message(self, event):
        @database_sync_to_async
        def set_last_read(response):
            print(response)
            member = ChatRoomMember.objects.get(chat_room = response['chat_room'],user = self.scope["user"])
            last_message = ChatMessage.objects.get(num = response['num'],chat_room = response['chat_room'])
            member.last_read = last_message
            member.save()

        response = event.copy()
        await set_last_read(response)
        await self.send(text_data=json.dumps(response))
        await self.channel_layer.group_send(f'chat_{response["chat_room"]}', {
            'type' : 'update.read',
            'chat_room' : response['chat_room'],
            'user' : self.scope["user"].email,
            'read' : response['num']
        })


    async def get_sync_message(self,chat_room=None):
        try:
            @database_sync_to_async
            def get_sync_data(user):
                serializer = SyncMessageSerializer(user.membership,many=True)
                return serializer.data
            
            @database_sync_to_async
            def get_user_list():
                user_list = chat_room.users.all()
                return list(user_list)
            
            if chat_room:
                user_list = await get_user_list()
                for user in user_list:
                    serializer_data = await get_sync_data(user)
                    await self.channel_layer.group_send(f'base_{user.username}', {'type' : 'sync.message','data':serializer_data})  
            else :
                serializer_data = await get_sync_data(self.scope['user'])
                await self.channel_layer.group_send(self.room_group_name, {'type' : 'sync.message','data':serializer_data})
        except Exception as e:
            print(e)

    async def receive_chat(self, message_data):
        @database_sync_to_async
        def get_room(request):
            if request.get('chat_room'):
                return ChatRoom.objects.get(name = request.get('chat_room'))
            raise ValueError('잘못된 chat_room 기입')

        @database_sync_to_async
        def create_message(chat_room,sender,content):
            existing_messages = ChatMessage.objects.filter(chat_room = chat_room)
            message = ChatMessage.objects.create(
                    chat_room = chat_room,
                    sender = sender,
                    content = content,
                    num = existing_messages.count() + 1
                )
            chat_room.last_message = message
            chat_room.save()
            return message

        @SyncToAsync
        def save_message(key,data):
            data_to_json = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.redis.rpush(key, data_to_json)
            self.redis.expire(key, 60*60*24*7)

        chat_room = await get_room(message_data['request'])
        message = await create_message(
                    chat_room = chat_room,
                    sender = self.scope['user'],
                    content = message_data['content']
                )
        
        serializer = ChatMessageSerializer(message)
        room_group_name = f"chat_{message_data['request']['chat_room']}"
        await save_message(room_group_name, serializer.data)
        await self.channel_layer.group_send(room_group_name, serializer.data)
        await self.get_sync_message(chat_room)

    async def active_chat(self,message_data):
        @database_sync_to_async
        def get_last_message(chat_room):
            try:
                chat_room_object = ChatRoom.objects.get(name = chat_room)
                member = ChatRoomMember.objects.get(chat_room = chat_room,user = self.scope["user"])
                member.last_read = chat_room_object.last_message
                member.save()
                return chat_room_object.last_message.num if chat_room_object.last_message else 0
            except :
                raise ValueError("잘못된 chat_room 기입")
            
        @database_sync_to_async
        def get_users_info(chat_room):
            members = ChatRoomMember.objects.filter(chat_room = chat_room)
            members_data = ChatRoomMembersSerializer(members,many = True)
            return members_data.data

        try:
            room_group_name = f"chat_{message_data['request']['chat_room']}"
            await self.channel_layer.group_add(room_group_name, self.channel_name)
            await self.channel_layer.group_send(room_group_name, {
                'type' : 'update.read',
                'chat_room' : message_data['request']['chat_room'],
                'user' : self.scope["user"].email,
                'read' : await get_last_message(message_data['request']['chat_room'])
            })
            members_data = await get_users_info(message_data['request']['chat_room'])
            messages = [json.loads(i) for i in self.redis.lrange(room_group_name, 0, -1)]
            await self.send(text_data=json.dumps({'type':'chat_room.info','members':members_data,'messages':messages}))
        except Exception as e:
            await self.send(text_data=json.dumps({'type':'error','message':e}))

    async def deactive_chat(self,message_data):
        room_group_name = f"chat_{message_data['request']['chat_room']}"
        await self.channel_layer.group_discard(room_group_name, self.channel_name)

    async def update_read(self, event):
        await self.send(text_data=json.dumps(event))

    async def sync_message(self, event):
        await self.send(text_data=json.dumps(event))