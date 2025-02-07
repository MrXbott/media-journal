from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError



class Parameter(models.Model):
    TYPE_CHOICES = (
        ('default_user_photo', 'Default User Photo'),
    )
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=False, null=False)

    class Meta:
        abstract = True

class Image(Parameter):
    image = models.ImageField(upload_to='default/', blank=False, null=False)

    def preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100"/>')
    
    def clean(self):
        if not self.pk and Image.objects.exists():
            raise ValidationError('You can\'t create one more object of this type')
        
