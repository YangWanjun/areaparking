import googlemaps

from django.db.models import Min, Count, Prefetch, Func, F

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from . import models, serializers
from master.models import Config


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


class GeocodeViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        address = request.GET.get('address', None)
        coordinate = {'lng': 0, 'lat': 0}
        api_key = Config.get_google_map_key()
        if address and api_key:
            gmap = googlemaps.Client(key=api_key)
            geocode_result = gmap.geocode(address)
            if len(geocode_result) > 0 and 'geometry' in geocode_result[0]:
                geometry = geocode_result[0].get('geometry')
                address_components = geocode_result[0].get('address_components')
                countries = [item for item in address_components if item.get('short_name').upper() == "JP"]
                if len(countries) > 0:
                    coordinate = geometry.get('location')
        return Response(coordinate)

