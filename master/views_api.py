from rest_framework import viewsets
from rest_framework.filters import SearchFilter, DjangoFilterBackend

from . import models, serializers


# Create your views here.
class CarMakerViewSet(viewsets.ModelViewSet):
    queryset = models.CarMaker.objects.public_all()
    serializer_class = serializers.CarMakerSerializer
    filter_backends = [SearchFilter]
    search_fields = ('name',)


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = models.CarModel.objects.public_all()
    serializer_class = serializers.CarModelSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_fields = ('maker__name',)
    search_fields = ('name', 'grade_name')
