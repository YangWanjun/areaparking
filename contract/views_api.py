from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models, serializers
from utils import constants


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = models.Subscription.objects.public_all()
    serializer_class = serializers.SubscriptionSerializer


class TempContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.temp_objects.public_all()
    serializer_class = serializers.ContractSerializer


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = models.Process.objects.public_all()
    serializer_class = serializers.ProcessSerializer


class ContractCancellation(viewsets.ModelViewSet):
    queryset = models.ContractCancellation.objects.public_all()
    serializer_class = serializers.ContractCancellationApiSerializer


class ParkingLotCancellationViewSet(viewsets.ModelViewSet):
    queryset = models.ParkingLotCancellation.objects.public_all()
    serializer_class = serializers.ParkingLotCancellationSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        data['created_user'] = request.user.pk
        for key in data.keys():
            val = data.get(key, None)
            if val and isinstance(val, list):
                data[key] = (val[0] or None) if len(val) > 0 else None
                if len(val) == 0:
                    data[key] = None
                elif len(val) == 1:
                    data[key] = val[0] or None
                else:
                    data[key] = ",".join(val)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['PUT'])
def task_finish(request, pk):
    """タスクを完了するＡＰＩ

    :param request:
    :param pk:
    :return:
    """
    task = get_object_or_404(models.Task, pk=pk)
    prev_task = task.get_prev_task()

    if request.method == 'PUT':
        if prev_task is None or prev_task.can_continue():
            task.status = '99'
            task.save()
            serializer = serializers.TaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response({'detail': constants.ERROR_PREV_TASK_UNFINISHED}, status=400)


@api_view(['PUT'])
def task_skip(request, pk):
    """タスクを完了するＡＰＩ

    :param request:
    :param pk:
    :return:
    """
    task = get_object_or_404(models.Task, pk=pk)
    prev_task = task.get_prev_task()

    if request.method == 'PUT':
        if prev_task is None or prev_task.can_continue():
            task.status = '10'
            task.save()
            serializer = serializers.TaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response({'detail': constants.ERROR_PREV_TASK_UNFINISHED}, status=400)


@api_view(['PUT'])
def task_undo(request, pk):
    """タスクを未実施の状態に戻るＡＰＩ

    :param request:
    :param pk:
    :return:
    """
    task = get_object_or_404(models.Task, pk=pk)

    if request.method == 'PUT' and task.status != '01':
        task.status = '01'
        task.save()
        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data)


@api_view(['PUT'])
def task_cancel(request, pk):
    """タスクを完了するＡＰＩ

    :param request:
    :param pk:
    :return:
    """
    task = get_object_or_404(models.Task, pk=pk)

    if request.method == 'PUT' and task.is_end:
        task.status = '91'
        task.save()
        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data)
