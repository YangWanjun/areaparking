from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

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
    list_display = ('name', 'parking_lot', 'parking_position', 'percent', 'contract_start_date', 'created_date')
    detail_view_class = SubscriptionDetailView
    list_view_class = SubscriptionListView

    # def has_change_permission(self, request, obj=None):
    #     return False


class SubscriptionFinish(BaseView):
    def get(self, request, *args, **kwargs):
        contract = get_object_or_404(models.Contract, pk=kwargs.get('pk'))
        contract.status = '11'
        contract.contractor.status = '11'
        contract.save()
        contract.contractor.save()
        return redirect('contract:tempcontract_list')


class SubscriptionDestroy(BaseView):
    def get(self, request, *args, **kwargs):
        contract = get_object_or_404(models.Contract, pk=kwargs.get('pk'))
        contract.status = '21'
        contract.contractor.status = '21'
        contract.save()
        contract.contractor.save()
        return redirect('contract:tempcontract_list')


class ContractVewSet(BaseModelViewSet):
    model = models.Contract
    queryset = models.Contract.real_objects.public_all()
    list_display = ('id', 'contractor', 'parking_lot', 'parking_position', 'start_date', 'end_date')


class ContractorVewSet(BaseModelViewSet):
    model = models.Contractor
    queryset = models.Contractor.real_objects.public_all()
    list_display = ('code', 'get_category_display', 'name', 'tel', 'email', 'address1')
    list_display_links = ('code', 'name',)


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
