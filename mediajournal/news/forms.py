from django import forms

from .models import News

class SuggestNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text']

    def __init__(self, *args, **kwargs):
        super(SuggestNewsForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Заголовок новости'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['placeholder'] = 'Текст новости'
        self.fields['text'].widget.attrs['class'] = 'form-control'