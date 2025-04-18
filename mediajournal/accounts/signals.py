from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from subscriptions.models import Subscriber 


@receiver(post_save, sender=User)
def link_subscriber_to_user(sender, instance, created, **kwargs):
    if created:
        try:
            subscriber = Subscriber.objects.get(email=instance.email, user=None)
            subscriber.user = instance
            subscriber.save()
        except Subscriber.DoesNotExist:
            pass
