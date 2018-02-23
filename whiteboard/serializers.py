from django.contrib.gis.geos import Point

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField

from . import models
from employee.serializers import MemberSerializer
from utils.django_base import BaseModelSerializer


class WhiteBoardSerializer(GeoFeatureModelSerializer):
    point = GeometrySerializerMethodField()
    staff = MemberSerializer()
    empty_count = serializers.SerializerMethodField()

    class Meta:
        model = models.WhiteBoard
        fields = '__all__'
        geo_field = 'point'

    def get_point(self, obj):
        return Point(obj.lng or 0, obj.lat or 0, srid=4326)

    def get_empty_count(self, obj):
        """空きの車室数を取得する。

        :param obj:
        :return:
        """
        return obj.position_count - obj.contract_count - obj.temp_contract_count


class WhiteBoardPositionSerializer(BaseModelSerializer):

    class Meta:
        model = models.WhiteBoardPosition
        fields = '__all__'


class InquirySerializer(BaseModelSerializer):

    class Meta:
        model = models.Inquiry
        fields = '__all__'


class WaitingSerializer(BaseModelSerializer):

    class Meta:
        model = models.Waiting
        fields = '__all__'
