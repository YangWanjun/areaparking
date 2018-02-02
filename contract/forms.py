# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from . import models
from utils.django_base import BaseForm


class ContractorForm(BaseForm):
    class Meta:
        model = models.Contractor
        fields = '__all__'

    # def clean(self):
    #     cleaned_data = super(ContractorForm, self).clean()
    #     segment = cleaned_data.get('segment', None)
    #     name = cleaned_data.get('name', None)
    #     corporate_president = cleaned_data.get('corporate_president', None)
    #     corporate_staff_name = cleaned_data.get('corporate_staff_name', None)
    #     if segment and segment == '1':
    #         # 個人の場合
    #         if not name:
    #             self.add_error('name', "個人の場合、契約者の名前を入力してください。")
    #     elif segment and segment == '2':
    #         # 法人の場合
    #         if not corporate_president:
    #             self.add_error('president', "法人の場合、代表者名を入力してください。")
    #         if not corporate_staff_name:
    #             self.add_error('staff_name', "法人の場合、担当者名を入力してください。")
    #     return cleaned_data


class SubscriptionForm(BaseForm):
    class Meta:
        model = models.Subscription
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['parking_lot_id'].widget = forms.HiddenInput()
        self.fields['parking_position_id'].widget = forms.HiddenInput()


class ContractForm(BaseForm):
    class Meta:
        model = models.Contract
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.contractor:
                self.fields['contractor'].queryset = models.Contractor.objects.filter(pk=self.instance.contractor.pk)
            else:
                self.fields['subscription'].queryset = models.Subscription.objects.filter(pk=self.instance.subscription.pk)
            self.fields['parking_lot'].queryset = models.ParkingLot.objects.filter(pk=self.instance.parking_lot.pk)
            self.fields['parking_position'].queryset = models.ParkingPosition.objects.filter(
                parking_lot=self.instance.parking_lot)


class ProcessForm(BaseForm):
    class Meta:
        model = models.Process
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['name'].widget = forms.HiddenInput()
        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()


class ContractCancellationForm(BaseForm):
    class Meta:
        model = models.ContractCancellation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['contract'].widget = forms.HiddenInput()
        self.fields['parking_lot'].widget = forms.HiddenInput()
        self.fields['parking_position'].widget = forms.HiddenInput()
        self.fields['contractor'].widget = forms.HiddenInput()
        self.fields['reception_user'].widget = forms.HiddenInput()
        self.fields['cancellation_date'].widget.attrs.update({'class': 'vDateField'})
        self.fields['retire_date'].widget.attrs.update({'class': 'vDateField'})


class ParkingLotCancellationForm(BaseForm):

    class Meta:
        model = models.ParkingLotCancellation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['parking_lot'].widget = forms.HiddenInput()
        self.fields['is_all'].widget.attrs.update({'class': 'filled-in'})
        self.fields['is_immediately'].widget.attrs.update({'class': 'filled-in'})
        self.fields['is_with_continue'].widget.attrs.update({'class': 'filled-in'})
        self.fields['contact_date'].widget.attrs.update({'class': 'vDateField'})
        self.fields['return_date'].widget.attrs.update({'class': 'vDateField'})
