# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.geos import Point

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField

from . import models


class ParkingLotSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='buken.bk_name')
    class Meta:
        model = models.ParkingLot
        fields = ('id', 'label')

# class ParkingLotSummarySerializer(GeoFeatureModelSerializer):
#     point = GeometrySerializerMethodField()
#
#     class Meta:
#         model = models.VParkingLotSummary
#         fields = '__all__'
#         geo_field = 'point'
#
#     def get_point(self, obj):
#         return Point(obj.lng, obj.lat, srid=4326)
