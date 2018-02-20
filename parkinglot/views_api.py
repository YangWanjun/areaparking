from django.db.models import Min, Count, Prefetch, Func, F

from rest_framework import viewsets
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
