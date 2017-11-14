# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class CarMakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarMaker
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name3')

    class Meta:
        model = models.CarModel
        fields = ('id', 'maker', 'name', 'grade_name', 'sale_date', 'length', 'width', 'height', 'weight', 'f_value', 'r_value', 'min_height', 'full_name')

    def get_full_name3(self, obj):
        if obj.grade_name:
            return '%s - %s' % (obj.name, obj.grade_name)
        else:
            return obj.name
