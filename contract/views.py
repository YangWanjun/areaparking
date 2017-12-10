# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from . import models
from utils.django_base import BaseTemplateView, BaseView
from utils.mail import EbMail
from master import biz


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
        subscription_group = biz.get_subscription_mail_info()
        context.update({
            'temp_contract': temp_contract,
            'contractor': contractor,
            'parkingposition': parkingposition,
            'subscription_group': subscription_group,
        })
        return context


class SendSubscriptionMail(BaseView):
    def post(self, request, *args, **kwargs):
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
        mail = EbMail(**mail_data)
        mail.send_email()
