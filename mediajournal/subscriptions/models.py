from django.db import models

from accounts.models import User


class Subscriber(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email
