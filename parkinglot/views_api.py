from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min, Count, Prefetch, Func, F
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from . import models, serializers


# Create your views here.
class TargetParkingLotViewSet(viewsets.ModelViewSet):
    queryset = models.ParkingLot.objects.public_all()
    serializer_class = serializers.TargetParkingLotSerializer
    filter_backends = [SearchFilter]
    search_fields = ('name',)


class ParkingPositionSizeGrouped(viewsets.ViewSet):

    def list(self, request):
        code = request.GET.get('code', None)
        positions = []
        if code:
            queryset = models.ParkingPosition.objects.public_filter(parking_lot=code).order_by().values(
                'parking_lot', 'length', 'width', 'height', 'weight'
            ).annotate(
                count=Count('id'),
                price_recruitment=Min('price_recruitment'),
                price_recruitment_no_tax=Min('price_recruitment_no_tax'),
                price_homepage=Min('price_homepage'),
                price_homepage_no_tax=Min('price_homepage_no_tax'),
                price_handbill=Min('price_handbill'),
                price_handbill_no_tax=Min('price_handbill_no_tax'),
            ).prefetch_related(
                Prefetch(''),
            )
            for position in queryset:
                grouped_queryset = models.ParkingPosition.objects.public_filter(
                    parking_lot=code,
                    length=position.get('length'),
                    width=position.get('width'),
                    height=position.get('height'),
                    weight=position.get('weight'),
                ).annotate(
                    status=Func(F('id'), function='get_position_status')
                ).values('id', 'name', 'status')
                position['sub_positions'] = list(grouped_queryset)
                # このサイズすべての車室を契約状態を設定
                if len([pos for pos in position['sub_positions'] if pos['status'] == '01']) > 0:
                    # 空き
                    position['status'] = '01'
                elif len([pos for pos in position['sub_positions'] if pos['status'] == '02']) > 0:
                    # 手続中
                    position['status'] = '02'
                elif len([pos for pos in position['sub_positions'] if pos['status'] == '03']) == len(
                        position['sub_positions']):
                    # 空無
                    position['status'] = '03'
                else:
                    # 仮押さえ
                    position['status'] = '04'
                positions.append(position)

        return Response(positions)


class ManagementCompanyViewSet(viewsets.ModelViewSet):
    queryset = models.ManagementCompany.objects.public_all()
    serializer_class = serializers.ManagementCompanySerializer


@api_view(['PUT'])
def parking_position_lock(request, pk):
    """貸止め

    :param request:
    :param pk:
    :return:
    """
    parking_position = get_object_or_404(models.ParkingPosition, pk=pk)
    lock_object_id = request.data.get('lock_object_id')
    lock_content_type_id = request.data.get('lock_content_type_id')
    lock_reason = request.data.get('lock_reason')
    json = dict()
    if lock_object_id and lock_content_type_id and lock_reason:
        try:
            content_type = ContentType.objects.get(pk=lock_content_type_id)
            parking_position.is_lock = True
            parking_position.lock_content_type = content_type
            parking_position.lock_object_id = lock_object_id
            parking_position.lock_reason = lock_reason
            parking_position.save()
            serializer = serializers.ParkingPositionSerializer(parking_position)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            json.update({
                'lock_content_object_name': ["選択された項目種類は登録されていません。"]
            })
    else:
        if not lock_object_id:
            json.update({
                'lock_content_object_name': ["この項目は空にできません。"]
            })
        if not lock_content_type_id:
            json.update({
                'lock_content_object_name': ["この項目は空にできません。"]
            })
        if not lock_reason:
            json.update({
                'lock_reason': ["この項目は空にできません。"]
            })
    return Response(json, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def parking_position_unlock(request, pk):
    """貸止め解除

    :param request:
    :param pk:
    :return:
    """
    parking_position = get_object_or_404(models.ParkingPosition, pk=pk)
    parking_position.is_lock = False
    parking_position.save()
    serializer = serializers.ParkingPositionSerializer(parking_position)
    return Response(serializer.data)
