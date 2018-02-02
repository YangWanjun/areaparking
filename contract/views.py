import datetime
import operator

from functools import reduce

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.template.context_processors import csrf

from . import models, biz, forms
from contract.models import Task
from format.models import ReportSubscriptionConfirm, ReportSubscription
from parkinglot.models import ParkingLot
from utils import common
from utils.django_base import BaseView, BaseDetailModelView, BaseListModelView, BaseModelViewSet, BaseTemplateView


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('contract:subscription_list')


class SubscriptionDetailView(BaseDetailModelView):
    def get_context_data(self, **kwargs):
        context = super(SubscriptionDetailView, self).get_context_data(**kwargs)
        context.update({
            'subscription_confirm_template': ReportSubscriptionConfirm.get_default_report(),
            'subscription_template': ReportSubscription.get_default_report(),
        })
        return context


class SubscriptionListView(BaseListModelView):
    pass


class SubscriptionVewSet(BaseModelViewSet):
    model = models.Subscription
    queryset = models.Subscription.temp_objects.public_all()
    list_display = ('name', 'parking_lot', 'parking_position', 'percent', 'contract_start_date', 'created_date')
    detail_view_class = SubscriptionDetailView
    list_view_class = SubscriptionListView

    # def has_change_permission(self, request, obj=None):
    #     return False


class SubscriptionFinish(BaseView):

    def post(self, request, *args, **kwargs):
        subscription = get_object_or_404(models.Subscription, pk=kwargs.get('pk'))
        try:
            # 契約情報を作成する
            contract = biz.subscription_to_contract(subscription)
            url = reverse('contract:contract_detail', args=(contract.pk,))
            # 成約
            subscription.status = '11'
            subscription.save()
            json = {'error': 0, 'url': url}
        except Exception as ex:
            json = {'error': 1, 'message': str(ex)}
        return JsonResponse(json)


class SubscriptionDestroy(BaseView):
    def get(self, request, *args, **kwargs):
        contract = get_object_or_404(models.Contract, pk=kwargs.get('pk'))
        contract.status = '21'
        contract.contractor.status = '21'
        contract.save()
        contract.contractor.save()
        return redirect('contract:tempcontract_list')


class ContractListView(BaseListModelView):

    def get_queryset(self, *args, **kwargs):
        queryset = super(ContractListView, self).get_queryset()
        q = self.request.GET.get('datatable-search[value]', None)
        if q:
            orm_lookups = ['parking_lot__name__icontains', 'contractor__name__icontains', 'staff__first_name__icontains', 'staff__last_name__icontains']
            for bit in q.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset

    def get_datatable_config(self):
        config = super(ContractListView, self).get_datatable_config()
        config['searching'] = True
        return config


class ContractDetailView(BaseDetailModelView):

    def get_context_data(self, **kwargs):
        context = super(ContractDetailView, self).get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(self.object)
        process_form = forms.ProcessForm(initial={'content_type': content_type, 'object_id': self.object.pk})
        contract_cancellation_form = forms.ContractCancellationForm(initial={
            'contract': self.object,
            'parking_lot': self.object.parking_lot,
            'parking_position': self.object.parking_position,
            'contractor': self.object.contractor,
            'reception_user': self.request.user,
        })
        context.update({
            'process_form': process_form,
            'contract_cancellation_form': contract_cancellation_form,
        })
        return context


class ContractVewSet(BaseModelViewSet):
    model = models.Contract
    queryset = models.Contract.real_objects.public_all()
    list_display = ('id', 'contractor', 'parking_lot', 'parking_position', 'staff', 'start_date', 'end_date')
    list_view_class = ContractListView
    detail_view_class = ContractDetailView


class ContractedParkingLotDetailView(BaseDetailModelView):

    def get_context_data(self, **kwargs):
        context = super(ContractedParkingLotDetailView, self).get_context_data(**kwargs)
        cancellation_form = forms.ParkingLotCancellationForm(initial={
            'parking_lot': self.object.parking_lot,
            'contact_date': datetime.date.today(),
        })
        context.update({
            'cancellation_form': cancellation_form,
        })
        return context


class ContractedParkingLotViewSet(BaseModelViewSet):
    model = models.VContractedParkingLot
    list_display = ('name', 'address', 'staff', 'owner', 'lease_management_company', 'building_management_company')
    detail_view_class = ContractedParkingLotDetailView

    def has_change_permission(self, request, obj=None):
        return False


class ContractorListView(BaseListModelView):

    def get_queryset(self, *args, **kwargs):
        queryset = super(ContractorListView, self).get_queryset()
        q = self.request.GET.get('datatable-search[value]', None)
        if q:
            orm_lookups = ['name__icontains', 'tel__icontains']
            for bit in q.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset

    def get_datatable_config(self):
        config = super(ContractorListView, self).get_datatable_config()
        config['searching'] = True
        return config


class ContractorVewSet(BaseModelViewSet):
    model = models.Contractor
    queryset = models.Contractor.real_objects.public_all()
    list_display = ('code', 'get_category_display', 'name', 'tel', 'email', 'address1')
    list_display_links = ('code', 'name',)
    list_view_class = ContractorListView

    def get_category_display(self, obj):
        return obj.get_category_display()
    get_category_display.short_description = '分類'


class ProcessViewSet(BaseModelViewSet):
    model = models.Process
    queryset = models.Process.objects.public_filter(name__gte='10')
    list_display = (
        'get_name_display', 'percent', 'contractor', 'parking_lot', 'parking_position', 'created_date'
    )

    def get_name_display(self, obj):
        return obj.get_name_display()
    get_name_display.short_description = '名称'

    def has_change_permission(self, request, obj=None):
        return False


class SendSubscriptionMail(BaseView):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('task_id'))
        subscription_url = request.POST.get('subscription_url', None)
        if not subscription_url:
            json = {'error': True, 'message': '少なくとも１つの申込書を選択してください。'}
        else:
            task.url_links = subscription_url
            sender = request.POST.get('subscription_sender', None)
            recipient_list = request.POST.get('subscription_to', None)
            cc_list = request.POST.get('subscription_cc', None)
            bcc_list = request.POST.get('subscription_bcc', None)
            mail_title = request.POST.get('subscription_title', None)
            mail_body = request.POST.get('subscription_content', None)
            mail_data = {
                'sender': sender, 'recipient_list': recipient_list, 'cc_list': cc_list,
                'bcc_list': bcc_list, 'mail_title': mail_title, 'mail_body': mail_body,
            }
            json = biz.send_mail_from_view(task, request, mail_data)
        return JsonResponse(json)


class SendContractMail(BaseView):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('task_id'))
        sender = request.POST.get('contract_sender', None)
        recipient_list = request.POST.get('contract_to', None)
        cc_list = request.POST.get('contract_cc', None)
        bcc_list = request.POST.get('contract_bcc', None)
        mail_title = request.POST.get('contract_title', None)
        mail_body = request.POST.get('contract_content', None)
        mail_data = {
            'sender': sender, 'recipient_list': recipient_list, 'cc_list': cc_list,
            'bcc_list': bcc_list, 'mail_title': mail_title, 'mail_body': mail_body,
        }
        json = biz.send_mail_from_view(task, request, mail_data)
        return JsonResponse(json)


class SendTaskMail(BaseView):

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('task_id'))
        sender = request.POST.get('mail_sender', None)
        recipient_list = request.POST.get('mail_to', None)
        cc_list = request.POST.get('mail_cc', None)
        bcc_list = request.POST.get('mail_bcc', None)
        mail_title = request.POST.get('mail_title', None)
        mail_body = request.POST.get('mail_content', None)
        mail_data = {
            'sender': sender, 'recipient_list': recipient_list, 'cc_list': cc_list,
            'bcc_list': bcc_list, 'mail_title': mail_title, 'mail_body': mail_body,
        }
        json = biz.send_mail_from_view(task, request, mail_data)
        return JsonResponse(json)


class PriceRaiseListView(BaseTemplateView):
    template_name = 'contract/priceraise_list.html'

    def get_context_data(self, **kwargs):
        context = super(PriceRaiseListView, self).get_context_data(**kwargs)
        year = self.request.GET.get('_year') or datetime.date.today().strftime('%Y')
        month = self.request.GET.get('_month') or datetime.date.today().strftime('%m')
        prev_month = common.add_months(datetime.date(int(year), int(month), 1), -1)
        next_month = common.add_months(datetime.date(int(year), int(month), 1), 1)
        object_list = models.VPriceRaise.objects.filter(year=year, month=month)
        context.update({
            'object_list': object_list,
            'year': year,
            'month': month,
            'prev_month': prev_month,
            'next_month': next_month,
        })
        context.update(csrf(self.request))
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        object_list = context.get('object_list')
        year = context.get('year')
        month = context.get('month')
        selected_objects = request.POST.getlist('selected_object')
        if object_list and selected_objects:
            object_list = object_list.filter(pk__in=selected_objects)
            for obj in object_list:
                try:
                    price_raising = models.PriceRaising(contract=obj.contract, contractor=obj.contractor)
                    price_raising.year = obj.year
                    price_raising.month = obj.month
                    price_raising.parking_lot = obj.parking_lot
                    price_raising.parking_position = obj.parking_position
                    price_raising.car = obj.car
                    price_raising.staff = obj.staff
                    price_raising.start_date = obj.start_date
                    price_raising.end_date = obj.end_date
                    price_raising.current_amount = obj.amount
                    price_raising.current_amount_with_tax = obj.amount_with_tax
                    price_raising.prev_amount = obj.prev_amount
                    price_raising.prev_amount_with_tax = obj.prev_amount_with_tax
                    price_raising.save()
                except Exception as ex:
                    common.get_ap_logger().error(ex)
        return redirect(reverse('contract:priceraising_list') + "?_year=%s&_month=%s" % (year, month))


class PriceRaisingListView(BaseTemplateView):
    template_name = 'contract/priceraising_list.html'

    def get_context_data(self, **kwargs):
        context = super(PriceRaisingListView, self).get_context_data(**kwargs)
        year = self.request.GET.get('_year') or datetime.date.today().strftime('%Y')
        month = self.request.GET.get('_month') or datetime.date.today().strftime('%m')
        prev_month = common.add_months(datetime.date(int(year), int(month), 1), -1)
        next_month = common.add_months(datetime.date(int(year), int(month), 1), 1)
        object_list = models.PriceRaising.objects.filter(year=year, month=month)
        context.update({
            'object_list': object_list,
            'year': year,
            'month': month,
            'prev_month': prev_month,
            'next_month': next_month,
        })
        return context


class TroubleListView(BaseTemplateView):
    template_name = 'contract/trouble_list.html'


class TroubleDetailView(BaseTemplateView):
    template_name = 'contract/trouble_detail.html'


class TroubleAddView(BaseTemplateView):
    template_name = 'contract/trouble_add.html'


class DefectListView(BaseTemplateView):
    template_name = 'contract/defect_list.html'


class DefectDetailView(BaseTemplateView):
    template_name = 'contract/defect_detail.html'


class DefectAddView(BaseTemplateView):
    template_name = 'contract/defect_add.html'


class VoluntaryInsuranceListView(BaseTemplateView):
    template_name = 'contract/voluntary_insurance_list.html'


class ParkingLotCancellationViewSet(BaseModelViewSet):
    model = models.ParkingLotCancellation
    list_display = ('parking_lot', 'get_parking_positions', 'is_immediately', 'is_with_continue', 'contact_date', 'return_date')

    def get_parking_positions(self, obj):
        if obj.is_all:
            return "全件"
        else:
            return obj.parking_positions
    get_parking_positions.short_description = "返却車室"
