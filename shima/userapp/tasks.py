import requests
from celery import shared_task
from userapp.models import Users,Payment,Attendance
import logging

@shared_task
def asign_payment():
    logging.info()
    pass

@shared_task
def asign_attendance():
    users=Users.objects.all()
    for user in users:
        try:
            Attendance.objects.create(user=user,is_present=False)
        except:
            pass
    