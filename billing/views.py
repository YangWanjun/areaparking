import operator

from functools import reduce

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.template.context_processors import csrf

from . import biz, models
from utils import constants
from utils.django_base import BaseView, BaseTemplateView, BaseModelViewSet, BaseDetailModelView


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('billing:import_transfer')


class ImportTransfer(BaseTemplateView):
    template_name = 'billing/import_transfer.html'

    def get_context_data(self, **kwargs):
        context = super(ImportTransfer, self).get_context_data(**kwargs)
        context.update(csrf(self.request))
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'transfer' in request.FILES:
            input_data = request.FILES['transfer']
            biz.load_transfer_data(input_data.read(), request.user)
        else:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRE_TRANSFER_DATA)
        return self.render_to_response(context)


class ArrearsListView(BaseTemplateView):
    template_name = 'billing/arrears_list.html'


class TransferDetailView(BaseDetailModelView):
    template_name = 'billing/transferheader_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TransferDetailView, self).get_context_data(**kwargs)
        details = self.object.vtransferdetail_set.all()
        q = self.request.GET.get('q', None)
        if q:
            orm_lookups = ['nominee_name__icontains', 'contractor__name__icontains', 'parking_lot__name__icontains']
            for bit in q.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                details = details.filter(reduce(operator.or_, or_queries))
        status = self.request.GET.get('status', None)
        if status:
            details = details.filter(status=status)
        context.update({
            'details': details,
            'status_list': constants.CHOICE_TRANSFER_STATUS,
        })
        return context


class TransferViewSet(BaseModelViewSet):
    model = models.TransferHeader
    list_display = ('created_date', 'created_ymd', 'bank_name', 'branch_name', 'account_number', 'balance')
    detail_view_class = TransferDetailView

    def has_change_permission(self, request, obj=None):
        return False
