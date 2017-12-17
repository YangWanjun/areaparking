from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers


class TempContractorViewSet(viewsets.ModelViewSet):
    queryset = models.TempContractor.objects.public_all()
    serializer_class = serializers.TempContractorSerializer


class TempContractViewSet(viewsets.ModelViewSet):
    queryset = models.TempContract.objects.public_all()
    serializer_class = serializers.TempContractSerializer
