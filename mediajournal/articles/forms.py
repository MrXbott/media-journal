from django import forms

from .models import Comment


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['body']

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True, label='comment')
    # article_id = forms.IntegerField(widget=forms.HiddenInput)
