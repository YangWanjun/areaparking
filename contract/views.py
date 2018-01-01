import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse

from . import models
from contract.models import Task
from format.models import ReportSubscriptionConfirm, ReportSubscription
from utils.django_base import BaseView, BaseDetailModelView, BaseListModelView, BaseModelViewSet
from utils.mail import EbMail


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('contract:tempcontract_list')


class TempContractDetailView(BaseDetailModelView):
    def get_context_data(self, **kwargs):
        context = super(TempContractDetailView, self).get_context_data(**kwargs)
        context.update({
            'subscription_confirm_template': ReportSubscriptionConfirm.get_default_report(),
            'subscription_template': ReportSubscription.get_default_report(),
            'change_url': reverse('admin:contract_contract_change', args=(self.object.pk,)) + '?_popup=1',
        })
        return context


class TempContractListView(BaseListModelView):
    pass


class TempContractVewSet(BaseModelViewSet):
    model = models.TempContract
    list_display = ('name', 'parking_lot', 'parking_position', 'percent', 'start_date', 'end_date')
    detail_view_class = TempContractDetailView
    list_view_class = TempContractListView

    # def has_change_permission(self, request, obj=None):
    #     return False


class TempContractFinish(BaseView):
    def get(self, request, *args, **kwargs):
        contract = get_object_or_404(models.Contract, pk=kwargs.get('pk'))
        contract.status = '11'
        contract.contractor.status = '11'
        contract.save()
        contract.contractor.save()
        return redirect('contract:tempcontract_list')


class TempContractDestroy(BaseView):
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
            return JsonResponse({'error': True, 'message': '少なくとも１つの申込書を選択してください。'})
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
        try:
            mail = EbMail(**mail_data)
            mail.send_email()
            task.status = '99'      # タスク完了
            task.updated_user = request.user
            task.url_links = subscription_url
            task.save()
            # # 申込書確認のタスクを実施中とする
            # next_task = task.get_next_task()
            # if next_task:
            #     next_task.status = '02'
            #     next_task.save()
            json = {
                'error': False,
                'updated_date': datetime.datetime.now(),
                'updated_user': '%s %s' % (request.user.last_name, request.user.first_name),
            }
        except Exception as ex:
            json = {
                'error': True,
                'message': str(ex)
            }
        return JsonResponse(json)
