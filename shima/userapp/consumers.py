# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from channels.auth import get_user
# # from jwt import

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         user = self.scope.get('user')

#         # if self.is_authenticated(user):
#         await self.accept()
#         await self.add_user_to_group(user)

#     async def disconnect(self, close_code):
#         user = await self.get_user_from_scope()
#         # if await self.is_authenticated(user):
#         await self.remove_user_from_group(user)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.send_notification_to_all_users(message)

#     @database_sync_to_async
#     def get_user_from_scope(self):
#         return get_user(self.scope)

#     @database_sync_to_async
#     def is_authenticated(self, user):
#         return user.is_authenticated

#     @database_sync_to_async
#     def add_user_to_group(self, user):
#         async_to_sync(self.channel_layer.group_add)(
#             "notifications", self.channel_name
#         )
    
#     # @database_sync_to_async
#     # def add_user_to_group(self, user):
#     #     async_to_sync(self.channel_layer.group_add)("notifications", self.channel_name)

#     @database_sync_to_async
#     def remove_user_from_group(self, user):
#         async_to_sync(self.channel_layer.group_discard)(
#             "notifications", self.channel_name
#         )
#     # @database_sync_to_async
#     # def remove_user_from_group(self, user):
#     #     async_to_sync(self.channel_layer.group_discard)("notifications", self.channel_name)

#     async def send_notification_to_all_users(self, message):
#         await self.channel_layer.group_send(
#             "notifications",
#             {
#                 'type': 'send.notification',
#                 'message': message,
#             }
#         )

#     async def send_notification(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
