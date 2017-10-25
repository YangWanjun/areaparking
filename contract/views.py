# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from . import models, serializers


# Create your views here.
class ContractorViewSet(viewsets.ModelViewSet):
    queryset = models.Contractor.objects.public_all()
    serializer_class = serializers.ContractorSerializer
