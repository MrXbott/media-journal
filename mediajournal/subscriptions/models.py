from django.db import models

from accounts.models import User


class Subscriber(models.Model):
    """
    Модель подписчика, содержащая информацию о статусе подписки и привязке к пользователю.
    """
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='subscription')
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email
