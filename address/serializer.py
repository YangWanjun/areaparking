from rest_framework import serializers

from . import models


class PrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pref
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class AzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aza
        fields = '__all__'


class PostcodeSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField(source='get_address')

    class Meta:
        model = models.Postcode
        fields = '__all__'

    def get_address(self, obj):
        return obj.address
