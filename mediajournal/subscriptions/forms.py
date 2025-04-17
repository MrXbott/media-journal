from django import forms

from .models import Subscriber

class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']