from rest_framework import viewsets

from . import models, serializers


class MapBoardViewSet(viewsets.ModelViewSet):
    queryset = models.VMapBoard.objects.all()
    serializer_class = serializers.MapBoardSerializer
