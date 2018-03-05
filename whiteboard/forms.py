from django import forms

from . import models
from parkinglot.models import ParkingLot
from utils.django_base import BaseForm, SearchSelect


class TroubleForm(BaseForm):
    class Meta:
        model = models.Trouble
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        # self.fields['parking_lot'].widget = SearchSelect(ParkingLot)

    parking_lot = forms.ModelChoiceField(queryset=ParkingLot.objects.public_all(),
                                         widget=SearchSelect(ParkingLot),
                                         label='駐車場')
