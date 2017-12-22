# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from . import models
from parkinglot.models import ParkingLot
from utils.django_base import BaseForm, DynamicListWidget


# class ParkingLotForm(BaseForm):
#     class Meta:
#         model = ParkingLot
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         instance = kwargs.get('instance', None)
#         if instance and isinstance(instance, models.WhiteBoard):
#             kwargs.update({'instance', instance.parking_lot})
#         forms.ModelForm.__init__(self, *args, **kwargs)
#         if self.instance and self.instance.pk:
#             pass


# class WaitingAddForm(BaseForm):
#     parking_lot = forms.CharField(widget=DynamicListWidget(), label="駐車場")
#
#     class Meta:
#         model = models.Waiting
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(WaitingAddForm, self).__init__(*args, **kwargs)
#         self.fields['parking_lot'].widget.form_instance = self
#         for name in ('parking_lot', 'car_maker', 'car_model'):
#             old_class = self.fields[name].widget.attrs.get('class')
#             new_class = (old_class + ' eb-autocomplete') if old_class else 'eb-autocomplete'
#             self.fields[name].widget.attrs.update({'class': new_class})
#         self.fields['parking_lot'].widget.attrs.update({
#             'eb-autocomplete-url': reverse('parkinglot-list'),
#             'eb-autocomplete-target-id': 'id_parking_lot',
#         })
#         self.fields['car_maker'].widget.attrs.update({'eb-autocomplete-url': reverse('carmaker-list')})
#         self.fields['car_model'].widget.attrs.update({
#             'eb-autocomplete-url': reverse('carmodel-list'),
#             'eb-autocomplete-parent-name': 'maker__name',
#             'eb-autocomplete-parent-field-id': 'id_car_maker',
#             'eb-autocomplete-related-fields': json.dumps({
#                 'id_length': 'length',
#                 'id_width': 'width',
#                 'id_height': 'height',
#                 'id_weight': 'weight',
#             }),
#         })
#
#     def clean(self):
#         cleaned_data = super(WaitingAddForm, self).clean()
#         parking_lot_id = cleaned_data.get('parking_lot', None)
#         if parking_lot_id:
#             try:
#                 parking_lot = models.ParkingLot.objects.get(pk=parking_lot_id)
#                 cleaned_data['parking_lot'] = parking_lot
#             except (ObjectDoesNotExist, MultipleObjectsReturned):
#                 self.add_error('parking_lot', "該当する駐車場がありません。")
#         return cleaned_data
#
#
# class WaitingForm(BaseForm):
#     class Meta:
#         model = models.Waiting
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(WaitingForm, self).__init__(*args, **kwargs)
#         if self.instance and self.instance.parking_lot:
#             self.fields['parking_lot'].queryset = models.ParkingLot.objects.public_filter(pk=self.instance.parking_lot.pk)
