from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    author = models.ForeignKey('accounts.User', related_name='comments', null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('Comment', blank=True, null=True, unique=False, on_delete=models.SET_NULL, related_name='answers')
    is_active = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, 
                                     on_delete=models.CASCADE, 
                                     blank=False, 
                                     null=False, 
                                     limit_choices_to={'model__in':('article', 'news')}
                                     )
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    @property
    def children(self):
        return Comment.objects.filter(parent=self, is_active=True)

    def __str__(self) -> str:
        return f'Comment by {self.author.username if self.author else "User deleted"} on {self.content_object.title}'