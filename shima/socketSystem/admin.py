from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(NotificationContent)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(MessageMedia)
