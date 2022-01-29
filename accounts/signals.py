from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from .models import UserProfile, UserScores, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserScores)
def add_rate_sum(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.get(id=instance.user.id)
        if instance.type == '1':
            profile.courtesy_rate_sum += instance.score
        elif instance.type == '2':
            profile.punctuality_rate_sum += instance.score
        elif instance.type == '3':
            profile.adequacy_rate_sum += instance.score
        profile.save()