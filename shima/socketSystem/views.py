from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from datetime import date
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from userapp.models import Users
from socketSystem.models import Message,MessageMedia,Notification,NotificationContent
from socketSystem.serializers import MessageSerializer,MessageMediaSerializer,NotificationContentSerializer,NotificationSerializer,NotificationGetSerializer
# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes=[IsAdminUser]
    def create(self, request, *args, **kwargs):
        # Create a NotificationContent object with the message
        content_message = request.data.get('content_message')
        content = NotificationContent.objects.create(message=content_message)
        # Get all users you want to send the notification to
        users = Users.objects.all()  # You might need to adjust this query

        # Create a Notification for each user
        notifications = []
        for user in users:
            notification = Notification(user=user, content=content)
            notifications.append(notification)

        # Bulk create the notifications
        Notification.objects.bulk_create(notifications)

        return Response({'message': 'Notifications sent to all users'}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        # This view returns a list of all notifications.
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # This view retrieves a single notification by its ID.
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # This view is used to update a notification by its ID.
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # This view is used to delete a notification by its ID.
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class Notification(ListAPIView):
    serializer_class=NotificationGetSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user,is_seen=False)
        
        return queryset

    