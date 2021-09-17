from django.contrib.auth import get_user_model
from gaming_platform.celery import app
from time import sleep
from .models import UserProfile


@app.task()
def cheking_acc(id):
    sleep(900)
    user = get_user_model().objects.get(id=id)
    if user.is_active == False:
        UserProfile.objects.get(user=user).delete()
        user.delete()
        return 'Deleted'
    return user.username
    