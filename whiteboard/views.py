# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters

from django.shortcuts import get_object_or_404, redirect

from material.frontend.views import ModelViewSet, ListModelView

from utils.django_base import BaseTemplateView, BaseView
from parkinglot import models as parkinglot_model
from contract.forms import ContractorForm
from . import models


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('whiteboard:whiteboard_list')


class WhiteBoardFilter(django_filters.FilterSet):
    class Meta:
        model = models.WhiteBoard
        fields = ['bk_no']


class WhiteBoardListView(ListModelView):
    # paginate_by = 25
    filterset_class = WhiteBoardFilter

    def get_template_names(self):
        templates = super(WhiteBoardListView, self).get_template_names()
        return templates

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardListView, self).get_context_data()
        return context


class WhiteBoardViewSet(ModelViewSet):
    model = models.WhiteBoard
    list_display = (
        'bk_no', 'parking_lot', 'parking_position', 'is_existed_contractor_allowed', 'is_new_contractor_allowed', 'free_end_date', 'time_limit_id',
        'address', 'price_recruitment', 'price_recruitment_no_tax', 'price_homepage', 'price_homepage_no_tax', 'price_handbill', 'price_handbill_no_tax',
        'length', 'width', 'height', 'weight', 'tyre_width', 'tyre_width_ap', 'min_height', 'min_height_ap', 'f_value', 'r_value', 'position_comment'
    )
    list_display_links = ('bk_no', 'parking_lot')
    list_view_class = WhiteBoardListView

    def has_add_permission(self, request):
        return False


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
