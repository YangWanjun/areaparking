from django import forms

from . import models
from utils.django_base import BaseForm


class WaitingContactForm(BaseForm):
    class Meta:
        model = models.WaitingContact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WaitingContactForm, self).__init__(*args, **kwargs)
        self.fields['waiting'].widget = forms.HiddenInput()
        self.fields['comment'].widget = forms.Textarea(attrs={'class': 'materialize-textarea'})
        self.fields['contact_date'].widget.attrs.update({'class': 'vDateField'})
