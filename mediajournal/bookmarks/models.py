from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Bookmark(models.Model):
    """
    Модель закладки для сохранения понравившихся пользователю статей.
    """
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookmarks')

    content_type = models.ForeignKey(ContentType, 
                                     on_delete=models.CASCADE, 
                                     blank=False, 
                                     null=False, 
                                     limit_choices_to={'model__in':('article', 'news')}
                                     )
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user_id', 'content_type', 'object_id'], name='unique_bookmark')]
        indexes = [models.Index(fields=['content_type', 'object_id']), ]

