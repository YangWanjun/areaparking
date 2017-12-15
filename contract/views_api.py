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


class SubscriptionUpdateView(APIView):

    def get_object(self, pk):
        try:
            return models.Task.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
