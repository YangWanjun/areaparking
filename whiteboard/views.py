# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from material.frontend.views import ModelViewSet

from utils.django_base import BaseTemplateView

from parkinglot import models as parkinglot_model
from contract.forms import ContractorForm
from . import models


# Create your views here.
class WhiteBoardViewSet(ModelViewSet):
    model = models.WhiteBoard


class ParkingPositionListView(BaseTemplateView):
    template_name = "./whiteboard/index.html"

    def get_context_data(self, **kwargs):
        context = super(ParkingPositionListView, self).get_context_data(**kwargs)
        queryset = parkinglot_model.ParkingPosition.objects.public_all().order_by()[:100]
        context.update({
            'queryset': queryset,
        })
        return context


class ParkingLotDetail(BaseTemplateView):
    template_name = "./whiteboard/parkinglot.html"

    def get_context_data(self, **kwargs):
        context = super(ParkingLotDetail, self).get_context_data(**kwargs)
        parkinglot = get_object_or_404(parkinglot_model.ParkingLot, pk=kwargs.get('id'))
        context.update({
            'parkinglot': parkinglot,
        })
        return context


class ParkingPositionDetail(BaseTemplateView):
    template_name = "./whiteboard/parkingposition.html"

    def get_context_data(self, **kwargs):
        context = super(ParkingPositionDetail, self).get_context_data(**kwargs)
        parkingposition = get_object_or_404(parkinglot_model.ParkingPosition, pk=kwargs.get('id'))
        contractor_form = ContractorForm()
        context.update({
            'parkingposition': parkingposition,
            'contractor_form': contractor_form,
        })
        return context


class WaitingListView(BaseTemplateView):
    template_name = "./whiteboard/waiting-list.html"
