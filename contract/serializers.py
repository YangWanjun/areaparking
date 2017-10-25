# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from . import models


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contractor
        fields = '__all__'
