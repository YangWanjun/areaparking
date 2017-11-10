# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from . import models
from revolution.models import BkMst
from utils.django_base import BaseForm


class ParkingLotForm(BaseForm):
    class Meta:
        model = models.ParkingLot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['buken'].queryset = BkMst.objects.filter(pk=self.instance.buken.pk)


class ParkingPositionForm(BaseForm):
    class Meta:
        model = models.ParkingPosition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['parking_lot'].queryset = models.ParkingLot.objects.filter(pk=self.instance.parking_lot.pk)
