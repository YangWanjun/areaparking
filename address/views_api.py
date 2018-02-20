from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from . import biz, models, serializers
from parkinglot.models import ParkingLot
from utils.django_base import BaseApiPagination


class PrefViewSet(viewsets.ModelViewSet):
    queryset = models.Pref.objects.public_all()
    serializer_class = serializers.PrefSerializer
    filter_fields = ('code', 'name')


class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.public_all()
    serializer_class = serializers.CitySerializer
    filter_fields = ('code', 'name')
    pagination_class = BaseApiPagination


class AzaViewSet(viewsets.ModelViewSet):
    queryset = models.Aza.objects.public_all()
    serializer_class = serializers.AzaSerializer
    filter_fields = ('code', 'name', 'city__code')
    pagination_class = BaseApiPagination


class PostcodeViewSet(viewsets.ModelViewSet):
    queryset = models.Postcode.objects.public_all()
    serializer_class = serializers.PostcodeSerializer
    filter_fields = ('post_code',)
    pagination_class = BaseApiPagination


class GeocodeViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        address = request.GET.get('address', None)
        coordinate = biz.geocode(address)
        return Response(coordinate)


class TargetAreaViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        search = request.GET.get('search', None)
        area_list = []
        if search:
            city_qs = models.City.objects.public_filter(name__startswith=search).values('code', 'name')
            for city in city_qs:
                area_list.append({'id': city.get('code'), 'label': city.get('name')})
            aza_qs = models.Aza.objects.public_filter(name__startswith=search).values('code', 'name')
            for aza in aza_qs:
                area_list.append({'id': aza.get('code'), 'label': aza.get('name')})
            lot_qs = ParkingLot.objects.public_filter(name__icontains=search).values('code', 'name')
            for lot in lot_qs:
                area_list.append({'id': lot.get('code'), 'label': lot.get('name')})
        return Response(area_list)


class TargetCityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.public_all()
    serializer_class = serializers.TargetCitySerializer
    filter_backends = [SearchFilter]
    search_fields = ('name',)


class TargetAzaViewSet(viewsets.ModelViewSet):
    queryset = models.Aza.objects.public_all()
    serializer_class = serializers.TargetAzaSerializer
    filter_backends = [SearchFilter]
    search_fields = ('name',)
