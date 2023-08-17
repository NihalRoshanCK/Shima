from channels.routing import ProtocolTypeRouter, URLRouter
from userapp.consumers import NotificationConsumer
from django.urls import path
from channels.auth import AuthMiddlewareStack

# from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/notifications/", NotificationConsumer.as_asgi()),
        ]),
    ),
})