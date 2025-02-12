from django import forms

from .models import Comment, Article


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['body']

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True, label='comment')
    

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'category']