# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views import generic

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'parking-lot', views.ParkingLotViewSet)
router.register(r'parking-lot-summary', views.ParkingLotSummaryViewSet)

urlpatterns = [
    # url('^parking-lot-autocomplete/$', views.ParkingLotAutocomplete.as_view(), name="parking_lot_autocomplete"),
]
