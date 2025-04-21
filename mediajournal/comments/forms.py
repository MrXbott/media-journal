from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментариев.

    Эта форма используется для ввода текста комментария, а также для привязки его к родительскому
    комментарию (если данный комментарий является ответом на другой комментарий) 
    и к объекту (статье, новости), к которому он относится.

    Атрибуты:
        text (forms.CharField): Текст комментария.
        parent (forms.IntegerField): Идентификатор родительского комментария, если это ответ.
        object_id (forms.IntegerField): Идентификатор объекта, к которому привязан комментарий.

    Метаданные:
        model (Comment): Модель, с которой связана форма.
        fields (list): Список полей формы.
        widgets (dict): Словарь, в котором скрыты поля 'parent' и 'object_id'.
    """
    class Meta:
        model = Comment
        fields = ['text', 'parent', 'object_id']
        widgets = {
            'object_id': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
        }