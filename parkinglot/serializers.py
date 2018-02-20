# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class TargetParkingLotSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='code')
    label = serializers.ReadOnlyField(source='name')

    class Meta:
        model = models.ParkingLot
        fields = ('id', 'label')

