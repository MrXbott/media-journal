from django import forms
from django.forms.models import inlineformset_factory

from .models import Comment, Article, ArticleImage


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True, label='comment')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'category']

ArticleImageFormSet = inlineformset_factory(Article, ArticleImage, fields=['image'], extra=2, can_delete=True, max_num=10,)