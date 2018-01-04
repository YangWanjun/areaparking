from django.db.models import Min

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from . import models, serializers


# Create your views here.
class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = models.ParkingLot.objects.public_all()
    serializer_class = serializers.ParkingLotSerializer
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
                price_recruitment=Min('price_recruitment'),
                price_recruitment_no_tax=Min('price_recruitment_no_tax'),
                price_homepage=Min('price_homepage'),
                price_homepage_no_tax=Min('price_homepage_no_tax'),
                price_handbill=Min('price_handbill'),
                price_handbill_no_tax=Min('price_handbill_no_tax'),
            )
            for position in queryset:
                positions.append(position)

        return Response(positions)
