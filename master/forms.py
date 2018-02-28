from django import forms

from . import models
from utils import constants
from utils.django_base import BaseForm

class ConfigForm(BaseForm):
    class Meta:
        model = models.Config
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance and isinstance(instance, models.Config):
            if instance.name == constants.CONFIG_DECIMAL_TYPE:
                self.fields['value'] = forms.ChoiceField(constants.CHOICE_DECIMAL_TYPE, required=True, label=u"設定値")


class EMailLogEntryForm(BaseForm):
    class Meta:
        model = models.EMailLogEntry
        exclude = ('pk',)

    def __init__(self, *args, **kwargs):
        super(EMailLogEntryForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.body:
            self.instance.body = self.instance.body.replace('\r', '').replace('\n', '')
