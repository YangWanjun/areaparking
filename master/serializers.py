# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class CarMakerSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name')

    class Meta:
        model = models.CarMaker
        fields = ('id', 'name', 'label')


class CarModelSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = models.CarModel
        fields = ('id', 'maker', 'name', 'grade_name', 'sale_date',
                  'length', 'width', 'height', 'weight', 'f_value', 'r_value', 'min_height',
                  'label')

    def get_label(self, obj):
        return '%s%s' % (obj.name, (' - ' + obj.grade_name) if obj.grade_name else '')
