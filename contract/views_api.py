from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models, serializers


class ContractorViewSet(viewsets.ModelViewSet):
    queryset = models.Contractor.objects.public_all()
    serializer_class = serializers.ContractorSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.public_all()
    serializer_class = serializers.ContractSerializer


@api_view(['PUT'])
def task_finish(request, pk):
    """タスクを完了するＡＰＩ

    :param request:
    :param pk:
    :return:
    """
    task = get_object_or_404(models.Task, pk=pk)

    if request.method == 'PUT':
        task.status = '99'
        task.save()
        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data)


@api_view(['PUT'])
def task_skip(request, pk):
    """タスクを完了するＡＰＩ

    :param request:
    :param pk:
    :return:
    """
    task = get_object_or_404(models.Task, pk=pk)

    if request.method == 'PUT':
        task.status = '10'
        task.save()
        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data)
