from rest_framework import serializers

from . import models
from utils.django_base import BaseModelSerializer


class CarMakerSerializer(BaseModelSerializer):
    label = serializers.CharField(source='name')

    class Meta:
        model = models.CarMaker
        fields = ('id', 'name', 'label')


class CarModelSerializer(BaseModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = models.CarModel
        fields = ('id', 'maker', 'name', 'grade_name', 'sale_date',
                  'length', 'width', 'height', 'weight', 'f_value', 'r_value', 'min_height',
                  'label')

    def get_label(self, obj):
        return '%s%s' % (obj.name, (' - ' + obj.grade_name) if obj.grade_name else '')


class ConfigSerializer(BaseModelSerializer):

    class Meta:
        model = models.Config
        fields = '__all__'
