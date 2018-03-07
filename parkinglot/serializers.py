from rest_framework import serializers

from . import models
from utils.django_base import BaseModelSerializer


class TargetParkingLotSerializer(BaseModelSerializer):
    id = serializers.ReadOnlyField(source='code')
    label = serializers.ReadOnlyField(source='name')

    class Meta:
        model = models.ParkingLot
        fields = ('id', 'label')


class ParkingPositionSerializer(BaseModelSerializer):

    class Meta:
        model = models.ParkingPosition
        fields = '__all__'


class ManagementCompanyStaffSerializer(BaseModelSerializer):

    class Meta:
        model = models.ManagementCompanyStaff
        fields = '__all__'


class ManagementCompanySerializer(BaseModelSerializer):
    staff_set = ManagementCompanyStaffSerializer(many=True)

    class Meta:
        model = models.ManagementCompany
        fields = '__all__'


class ParkingLotTypeSerializer(BaseModelSerializer):

    class Meta:
        model = models.ParkingLotType
        fields = '__all__'
