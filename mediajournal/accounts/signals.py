from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User

@receiver(post_save, sender=User)
def create_default_username(sender, instance, created, **kwargs):
    if created:
        instance.username = f'user{instance.id}'
        instance.save()