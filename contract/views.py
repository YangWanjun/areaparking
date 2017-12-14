import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from . import models
from contract.models import Task
from format.models import ReportSubscriptionConfirm
from utils.django_base import BaseTemplateView, BaseView
from utils.mail import EbMail


# Create your views here.
class TempContractListView(BaseTemplateView):
    template_name = "./contract/index.html"

    def get_context_data(self, **kwargs):
        context = super(TempContractListView, self).get_context_data(**kwargs)
        queryset = models.TempContract.objects.public_all().order_by()
        context.update({
            'queryset': queryset,
        })
        return context


class TempContractDetailView(BaseTemplateView):
    template_name = './contract/temp-contract.html'

    def get_context_data(self, **kwargs):
        context = super(TempContractDetailView, self).get_context_data(**kwargs)
        temp_contract = get_object_or_404(models.TempContract, pk=kwargs.get('id'))
        parkingposition = temp_contract.parking_position
        contractor = temp_contract.contractor
        context.update({
            'temp_contract': temp_contract,
            'contractor': contractor,
            'parkingposition': parkingposition,
            'subscription_confirm_template': ReportSubscriptionConfirm.get_default_report()
        })
        return context


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
            task.mail_sent_datetime = datetime.datetime.now()
            task.updated_user = request.user
            task.url_links = subscription_url
            task.save()
            json = {
                'error': False,
            }
        except Exception as ex:
            json = {
                'error': True,
                'message': str(ex)
            }
        return JsonResponse(json)
