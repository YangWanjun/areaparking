# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import operator

from django.db.models import Q

from rest_framework import viewsets

from . import models, serializers


# Create your views here.
class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = models.ParkingLot.objects.public_all()
    serializer_class = serializers.ParkingLotSerializer
    search_fields = ('buken__bk_name',)

    def get_queryset(self):
        queryset = super(ParkingLotViewSet, self).get_queryset()
        q = self.request.GET.get('search', None)
        if q:
            orm_lookups = [s + '__icontains' for s in self.search_fields]
            for bit in q.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset
