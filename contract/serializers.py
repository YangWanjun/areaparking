# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError

from rest_framework import serializers

from . import models


class TempContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TempContractor
        fields = '__all__'

    # def validate_name(self, value):
    #     segment = self.initial_data.get('segment', None)
    #     if segment == '1' and not value:
    #         raise ValidationError("個人の場合、契約者の名前を入力してください。")
    #     return value
    #
    # def validate_corporate_president(self, value):
    #     segment = self.initial_data.get('segment', None)
    #     if segment == '2' and not value:
    #         raise ValidationError("法人の場合、代表者名を入力してください。")
    #     return value
    #
    # def validate_corporate_staff_name(self, value):
    #     segment = self.initial_data.get('segment', None)
    #     if segment == '2' and not value:
    #         raise ValidationError("法人の場合、担当者名を入力してください。")
    #     return value


class TempContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TempContract
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'
