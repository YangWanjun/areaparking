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


class TempContractorForm(BaseForm):
    class Meta:
        model = models.TempContract
        fields = '__all__'

    def save(self, commit=True):
        return super(TempContractorForm, self).save(commit)
