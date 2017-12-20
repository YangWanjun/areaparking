from django import forms

from . import models
from utils import constants

class ConfigForm(forms.ModelForm):
    class Meta:
        model = models.Config
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance and isinstance(instance, models.Config):
            if instance.name == 'theme':
                self.fields['value'] = forms.ChoiceField(constants.CHOICE_DECIMAL_TYPE, required=True, label=u"設定値")
