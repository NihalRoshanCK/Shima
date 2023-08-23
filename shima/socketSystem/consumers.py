from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
import asyncio


def make_group_name(user_id):
    return f'chat_{user_id}'


@database_sync_to_async
def save_message(message: dict):
    from userapp.models import Users
    from socketSystem.serializers import MessageSerializer
    try:
        message['receiver_id'] = Users.objects.get(id=message.pop('receiver_id')).id
    except Users.DoesNotExist:
        raise ValueError('Receiver does not exist')

    serializer = MessageSerializer(data=message)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

class MessageConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.user = None

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close(code=1009)
            return
        self.user = self.scope['user']
        self.room_group_name = make_group_name(self.user.id)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive_json(self, content, **kwargs):
        if content['type'] == 'message':
            message_data = content['message']
            message_data['sender_id'] = self.user.id
            message = await save_message(message_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message',
                    'message': message
                }
            )
            if message['receiver']['id'] != self.user.id:
                await self.channel_layer.group_send(
                    make_group_name(message['receiver']['id']),
                    {
                        'type': 'message',
                        'message': message
                    }
                )

    async def message(self, event):
        await self.send_json(event)

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        await self.close(code=close_code)
        

@database_sync_to_async
def get_notification_count(user):
    from socketSystem.models import Notification,NotificationContent
    return Notification.objects.filter(user=user, is_seen=False).count()

@database_sync_to_async
def mark_notifications_as_seen(user):
    from socketSystem.models import Notification,NotificationContent
    notifications = Notification.objects.filter(user=user, is_seen=False)
    for notification in notifications:
        notification.seen = True
        notification.save()
        
@database_sync_to_async
def get_pending_notifications(user):
    from socketSystem.models import Notification,NotificationContent
    return list(Notification.objects.filter(user=user, is_seen=False))

@database_sync_to_async
def get_new_notifications(user):
    from socketSystem.models import Notification,NotificationContent
    notifications=Notification.objects.filter(user=user,is_seen=False)
    for notification in notifications:
        notification['message']=notification.content.message
        notification['created']=notification.content.created_at
    print(notifications)
    return notifications
    
    
class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close(code=1009)
            return
        await self.accept()
        
    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content, **kwargs):
        action = content.get('action')
        user = self.scope['user']

        if action == 'mark_as_seen':
            await mark_notifications_as_seen(user)
        if action =='see_notification_count':
            await self.send_notification_count()
        if action =='see_notification':
            await self.send_notifications()
    
    
        
    async def send_notification_count(self):
        user = self.scope['user']
        count = await get_notification_count(user)
        await self.send_json({'notification_count': count})
        
    async def send_notifications(self):
        user = self.scope['user']
        # while True:
        new_notifications = await get_new_notifications(user)
        if new_notifications:
            for notification in new_notifications:
                await self.send_json({
                    'action': 'new_notification',
                    'notification': {
                        'id': notification.content.id,
                        'message': notification.message,
                        'created':notification.created_at
                    }
                })