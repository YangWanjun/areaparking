from rest_framework import viewsets

from . import models, serializers


class TempContractorViewSet(viewsets.ModelViewSet):
    queryset = models.TempContractor.objects.public_all()
    serializer_class = serializers.TempContractorSerializer


class TempContractViewSet(viewsets.ModelViewSet):
    queryset = models.TempContract.objects.public_all()
    serializer_class = serializers.TempContractSerializer
