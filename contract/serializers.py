from django.db import models

from rest_framework import serializers

from . import models
from utils.django_base import BaseModelSerializer


class ContractorSerializer(BaseModelSerializer):
    class Meta:
        model = models.Contractor
        fields = '__all__'


class SubscriptionSerializer(BaseModelSerializer):

    class Meta:
        model = models.Subscription
        fields = '__all__'


class ContractSerializer(BaseModelSerializer):
    class Meta:
        model = models.Contract
        fields = '__all__'


class TaskSerializer(BaseModelSerializer):
    updated_user_name = serializers.SerializerMethodField(source='get_updated_user_name')

    class Meta:
        model = models.Task
        fields = '__all__'

    def get_updated_user_name(self, obj):
        if obj.updated_user:
            return '%s %s' % (obj.updated_user.last_name, obj.updated_user.first_name)
        else:
            return ''


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


class ParkingLotCancellationSerializer(BaseModelSerializer):

    class Meta:
        model = models.ParkingLotCancellation
        fields = '__all__'
