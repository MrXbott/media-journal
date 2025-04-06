from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent', 'object_id']
        widgets = {
            # 'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
        }