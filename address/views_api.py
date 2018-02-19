from rest_framework import viewsets
from rest_framework.response import Response

from . import biz, models, serializer
from utils.django_base import BaseApiPagination


class PrefViewSet(viewsets.ModelViewSet):
    queryset = models.Pref.objects.public_all()
    serializer_class = serializer.PrefSerializer
    filter_fields = ('code', 'name')


class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.public_all()
    serializer_class = serializer.CitySerializer
    filter_fields = ('code', 'name')
    pagination_class = BaseApiPagination


class AzaViewSet(viewsets.ModelViewSet):
    queryset = models.Aza.objects.public_all()
    serializer_class = serializer.AzaSerializer
    filter_fields = ('code', 'name', 'city__code')
    pagination_class = BaseApiPagination


class PostcodeViewSet(viewsets.ModelViewSet):
    queryset = models.Postcode.objects.public_all()
    serializer_class = serializer.PostcodeSerializer
    filter_fields = ('post_code',)
    pagination_class = BaseApiPagination


class GeocodeViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        address = request.GET.get('address', None)
        coordinate = biz.geocode(address)
        return Response(coordinate)
