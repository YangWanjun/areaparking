# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class ParkingLotSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='buken.bk_name')
    class Meta:
        model = models.ParkingLot
        fields = ('id', 'name')
