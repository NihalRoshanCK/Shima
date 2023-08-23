from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Users)
# admin.site.register(Notification)
admin.site.register(leave_application)
admin.site.register(Attendance)