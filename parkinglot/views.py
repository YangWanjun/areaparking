# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from material.frontend.views import ModelViewSet

from . import models

# Create your views here.

class ParkingLotViewSet(ModelViewSet):
    model = models.ParkingLot
