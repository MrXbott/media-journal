from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from subscriptions.models import Subscriber 


@receiver(post_save, sender=User)
def link_subscriber_to_user(sender, instance, created, **kwargs):
    """
    Связывает подписчика (Subscriber) с новым пользователем (User), если их email совпадает.

    Вызывается после создания нового пользователя. Если в таблице подписчиков существует
    запись с тем же email, но без связанного пользователя, то этот подписчик будет
    привязан к новому пользователю.

    Аргументы:
        sender (type): Модель, отправившая сигнал (обычно User).
        instance (User): Экземпляр пользователя, который был создан или обновлён.
        created (bool): Флаг, указывающий, что объект был создан, а не обновлён.
        kwargs (dict): Дополнительные аргументы, передаваемые в сигнал.
    """
    if created:
        try:
            subscriber = Subscriber.objects.get(email=instance.email, user=None)
            subscriber.user = instance
            subscriber.save()
        except Subscriber.DoesNotExist:
            pass
