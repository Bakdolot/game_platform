from django.core.mail import send_mail
from django.conf import settings
from gaming_platform.celery import app


@app.task()
def send_email(text):
    send_mail('Question', text, settings.EMAIL_FROM, [settings.EMAIL_TO], fail_silently=True)
    