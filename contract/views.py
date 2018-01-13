import operator

from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse

from . import models, biz
from contract.models import Task
from format.models import ReportSubscriptionConfirm, ReportSubscription
from utils.django_base import BaseView, BaseDetailModelView, BaseListModelView, BaseModelViewSet


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


class ContractVewSet(BaseModelViewSet):
    model = models.Contract
    queryset = models.Contract.real_objects.public_all()
    list_display = ('id', 'contractor', 'parking_lot', 'parking_position', 'staff', 'start_date', 'end_date')
    list_view_class = ContractListView


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
