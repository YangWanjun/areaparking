# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class ParkingLotSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='code')
    label = serializers.ReadOnlyField(source='name')

    class Meta:
        model = models.ParkingLot
        fields = ('id', 'label')


class ParkingPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ParkingPosition
        fields = (
            'parking_lot',
            'price_recruitment', 'price_recruitment_no_tax',
            'price_homepage', 'price_homepage_no_tax',
            'price_handbill', 'price_handbill_no_tax',
            'length', 'width', 'height', 'weight',
        )
