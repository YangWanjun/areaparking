# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from . import models
from parkinglot.models import ParkingLot
from utils.django_base import BaseForm, DynamicListWidget


class WaitingForm(BaseForm):
    parking_lot = forms.CharField(widget=DynamicListWidget(), label="駐車場")

    class Meta:
        model = models.Waiting
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WaitingForm, self).__init__(*args, **kwargs)
        self.fields['parking_lot'].widget.form_instance = self
        # instance = kwargs.get('instance', None)
        # data = kwargs.get('data')
        # if data:
        #     parking_lot = data.get('parking_lot')
        #     if parking_lot and instance:
        #         instance.parking_lot =

    def clean(self):
        cleaned_data = super(WaitingForm, self).clean()
        parking_lot_id = cleaned_data.get('parking_lot', None)
        if parking_lot_id:
            try:
                parking_lot = models.ParkingLot.objects.get(pk=parking_lot_id)
                cleaned_data['parking_lot'] = parking_lot
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                self.add_error('parking_lot', "該当する駐車場がありません。")
        return cleaned_data
