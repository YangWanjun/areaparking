import operator

from functools import reduce

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.template.context_processors import csrf
from django.utils.html import format_html

from . import biz, models
from whiteboard.models import WhiteBoard
from utils import constants
from utils.django_base import BaseView, BaseTemplateView, BaseModelViewSet, BaseDetailModelView, BaseListModelView


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
            header = biz.load_transfer_data(input_data.read(), request.user)
            if header:
                return redirect('billing:transferheader_detail', pk=header.pk)
            else:
                messages.add_message(request, messages.ERROR, constants.ERROR_FORMAT_BANK_TRANSFER_CANNOT_IMPORT)
        else:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRE_TRANSFER_DATA)
        return self.render_to_response(context)


# class ArrearsListView(BaseTemplateView):
#     template_name = 'billing/arrears_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ArrearsListView, self).get_context_data(**kwargs)
#         object_list = models.VArrears.objects.all()
#         context.update({
#             'object_list': object_list,
#         })
#         return context


class ArrearsListView(BaseListModelView):

    def format_column(self, item, field_name, value):
        if field_name == 'contractor':
            formatted = format_html(
                '<a href="{}">{}</a>', reverse('contract:contractor_detail', args=(item.contractor.pk,)), value
            )
        elif field_name == 'request':
            formatted = format_html(
                '<a href="{}">{}</a>', reverse('billing:contractor_detail', args=(item.contractor.pk,)), value
            )
        else:
            formatted = super(ArrearsListView, self).format_column(item, field_name, value)
        return formatted


class ArrearsViewSet(BaseModelViewSet):
    model = models.VArrears
    list_display = (
        'contractor', 'parking_lot', 'parking_position', 'limit_date', 'request', 'request_amount', 'transfer_amount'
    )
    list_view_class = ArrearsListView

    def has_change_permission(self, request, obj=None):
        return False


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
        is_committed = self.request.GET.get('is_committed', None)
        if is_committed == 'on':
            details = details.filter(is_committed=True)
        else:
            details = details.filter(is_committed=False)
        context.update({
            'details': details,
            'status_list': constants.CHOICE_TRANSFER_STATUS,
        })
        return context

    def post(self, request, *args, **kwargs):
        # transfer_header = get_object_or_404(models.TransferHeader, pk=kwargs.get('pk'))
        selected_details = request.POST.getlist('selected_detail')
        detail_id_list = biz.execute_transfer_details(selected_details)
        json = {'error': False, 'committed_count': len(selected_details)}
        if detail_id_list:
            json.update({
                'error': True,
                'detail_id_list': detail_id_list,
                'committed_count': len(selected_details) - len(detail_id_list)
            })
        return JsonResponse(json)


class TransferViewSet(BaseModelViewSet):
    model = models.TransferHeader
    list_display = ('created_date', 'created_ymd', 'bank_name', 'branch_name', 'account_number', 'balance')
    detail_view_class = TransferDetailView

    def has_change_permission(self, request, obj=None):
        return False


class ContractorDetailView(BaseDetailModelView):
    template_name = 'billing/contractor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorDetailView, self).get_context_data(**kwargs)
        contractor_request_list = self.object.vcontractorrequest_set.all().order_by('request__year', 'request__month')
        context.update({
            'contractor_request_list': contractor_request_list,
        })
        return context


class ContractorListView(BaseListModelView):

    def format_column(self, item, field_name, value):
        if field_name == 'name':
            formatted = format_html('<a href="{}">{}</a>', reverse('billing:contractor_detail', args=(item.pk,)), value)
        else:
            formatted = super(ContractorListView, self).format_column(item, field_name, value)
        return formatted


class ContractorVewSet(BaseModelViewSet):
    model = models.Contractor
    queryset = models.Contractor.real_objects.public_all()
    list_display = ('code', 'get_category_display', 'name', 'tel', 'email', 'address1')
    list_display_links = ('name',)
    detail_view_class = ContractorDetailView
    list_view_class = ContractorListView

    def get_category_display(self, obj):
        return obj.get_category_display()
    get_category_display.short_description = '分類'

    def has_change_permission(self, request, obj=None):
        return False


class ParkingLotListView(BaseListModelView):
    template_name = 'billing/parkinglot_list.html'

    def format_column(self, item, field_name, value):
        if field_name == 'code':
            formatted = format_html('<a href="{}">{}</a>', reverse('billing:whiteboard_detail', args=(item.pk,)), value)
        else:
            formatted = super(ParkingLotListView, self).format_column(item, field_name, value)
        return formatted


class ParkingLotDetailView(BaseDetailModelView):
    template_name = 'billing/parkinglot_detail.html'


class ParkingLotViewSet(BaseModelViewSet):
    model = WhiteBoard
    list_display = ('code', 'name', 'category', 'address')
    list_view_class = ParkingLotListView
    detail_view_class = ParkingLotDetailView

    def has_change_permission(self, request, obj=None):
        return False
