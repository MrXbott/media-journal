from django import forms
from django.forms.models import inlineformset_factory

from .models import Article, ArticleImage, ArticleSection


# class CommentForm(forms.Form):
#     text = forms.CharField(widget=forms.Textarea, required=True, label='comment')

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text', 'article', 'parent']
#         widgets = {
#             'article': forms.HiddenInput(),
#             'parent': forms.HiddenInput(),
#         }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'text', ]

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Заголовок статьи'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['category'].empty_label = 'Выберите раздел'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['placeholder'] = 'Лид текст'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        


class ArticleSectionForm(forms.ModelForm):
    class Meta:
        model = ArticleSection
        fields=['title', 'text', 'quote']

    def __init__(self, *args, **kwargs):
        super(ArticleSectionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Заголовок раздела (не обязательно)'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['placeholder'] = 'Текст'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['quote'].widget.attrs['placeholder'] = 'Умная цитата (не обязательно)'
        self.fields['quote'].widget.attrs['class'] = 'form-control'


# class ArticleImageForm(forms.ModelForm):
#     class Meta:
#         model = ArticleImage
#         fields = ['image']

ArticleSectionFormSet = inlineformset_factory(Article, ArticleSection, form=ArticleSectionForm , fields=['title', 'text', 'quote'], extra=1, can_delete=False, max_num=5)

ArticleImageFormSet = inlineformset_factory(Article, ArticleImage, fields=['image'], extra=2, can_delete=False, max_num=5,)
