# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from . import models
from utils.django_base import BaseModelSerializer


class ContractorSerializer(BaseModelSerializer):
    class Meta:
        model = models.Contractor
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


class SubscriptionSerializer(BaseModelSerializer):

    class Meta:
        model = models.Subscription
        fields = '__all__'


class ContractSerializer(BaseModelSerializer):
    class Meta:
        model = models.Contract
        fields = '__all__'


class TaskSerializer(BaseModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class ProcessSerializer(BaseModelSerializer):
    class Meta:
        model = models.Process
        fields = '__all__'


class ContractCancellationSerializer(BaseModelSerializer):
    class Meta:
        model = models.ContractCancellation
        fields = '__all__'


class ContractCancellationApiSerializer(BaseModelSerializer):
    process_id = serializers.SerializerMethodField(source='get_process_id')

    class Meta:
        model = models.ContractCancellation
        fields = ('id', 'contract', 'parking_lot', 'parking_position', 'contractor', 'cancellation_date', 'retire_date', 'reception_user', 'process_id')

    def get_process_id(self, obj):
        process = obj.process
        return process.pk if process else None
