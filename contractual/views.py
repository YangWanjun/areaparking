# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from material.frontend.views import CreateModelView

from . import models
from utils.django_base import BaseTemplateView
from parkinglot import models as parkinglot_model


# Create your views here.
class TempContractListView(BaseTemplateView):
    template_name = "./contractual/index.html"

    def get_context_data(self, **kwargs):
        context = super(TempContractListView, self).get_context_data(**kwargs)
        queryset = models.TempContract.objects.public_all().order_by()
        context.update({
            'queryset': queryset,
        })
        return context


class CreateTempContractView(CreateModelView):
    model = models.TempContract

    def get_initial(self):
        initial = self.initial
        parking_position_id = self.request.GET.get('parking_position_id', None)
        if parking_position_id:
            parking_position = get_object_or_404(models.ParkingPosition, pk=parking_position_id)
            initial.update({
                'parking_position': parking_position,
                'parking_lot': parking_position.parking_lot
            })
        contractor_id = self.request.GET.get('contractor', None)
        if contractor_id:
            contractor = get_object_or_404(models.Contractor, pk=contractor_id)
            initial.update({
                'contractor': contractor,
            })
        return initial

    def get_success_url(self):
        return reverse('contractual:tempcontract_detail', args=(self.object.pk,))


class TempContractDetailView(BaseTemplateView):
    template_name = './contractual/temp-contract.html'

    def get_context_data(self, **kwargs):
        context = super(TempContractDetailView, self).get_context_data(**kwargs)
        parkingposition = get_object_or_404(parkinglot_model.ParkingPosition, pk=kwargs.get('id'))
        context.update({
            'parkingposition': parkingposition,
        })
        return context
