from django import forms
from django.forms.models import inlineformset_factory

from .models import Comment, Article, ArticleImage, ArticleSection


# class CommentForm(forms.Form):
#     text = forms.CharField(widget=forms.Textarea, required=True, label='comment')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'article', 'parent']
        widgets = {
            'article': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'category']

# class ArticleImageForm(forms.ModelForm):
#     class Meta:
#         model = ArticleImage
#         fields = ['image']

ArticleSectionFormSet = inlineformset_factory(Article, ArticleSection, fields=['text'], extra=2, can_delete=True, max_num=10)

ArticleImageFormSet = inlineformset_factory(Article, ArticleImage, fields=['image'], extra=2, can_delete=True, max_num=10,)
