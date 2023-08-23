from django.urls import path

from socketSystem.consumers import MessageConsumer, NotificationConsumer

websocket_urlpatterns = [
    path('ws/messages/', MessageConsumer.as_asgi(), name='messages'),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]