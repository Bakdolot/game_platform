from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from .models import UserProfile, UserScores


@receiver(post_save, sender=UserProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserScores.objects.create(user=instance.user)