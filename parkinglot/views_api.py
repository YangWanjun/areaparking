from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from . import models, serializers


# Create your views here.
class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = models.ParkingLot.objects.public_all()
    serializer_class = serializers.ParkingLotSerializer
    filter_backends = [SearchFilter]
    search_fields = ('name',)
