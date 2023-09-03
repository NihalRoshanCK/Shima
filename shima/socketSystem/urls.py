from django.urls import path, include
from rest_framework.routers import DefaultRouter
from socketSystem.views import NotificationViewSet,NotificationView,MessageViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'message', MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('notification/get',NotificationView.as_view()),
]