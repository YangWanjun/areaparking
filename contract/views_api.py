from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers


class TempContractorViewSet(viewsets.ModelViewSet):
    queryset = models.TempContractor.objects.public_all()
    serializer_class = serializers.TempContractorSerializer


class TempContractViewSet(viewsets.ModelViewSet):
    queryset = models.TempContract.objects.public_all()
    serializer_class = serializers.TempContractSerializer


@api_view(['PUT'])
def task_finish(request, pk):
    task = get_object_or_404(models.Task, pk=pk)

    if request.method == 'PUT':
        task.status = '99'
        task.save()
        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data)
