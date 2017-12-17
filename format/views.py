import os
import datetime

from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from . import biz, models
from contract.models import Task, TempContractor
from parkinglot.models import ParkingLot
from utils import constants, common
from utils.django_base import BaseView, BaseTemplateView


# Create your views here.
class UserOperationView(BaseTemplateView):
    template_name = 'format/format_base.html'

    def get_context_data(self, **kwargs):
        context = super(UserOperationView, self).get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get('task_id'))
        if task.url_links:
            urls = [url for url in task.url_links.split(',') if url]
            context.update({'urls': urls})
        return context


class SubscriptionConfirmView(BaseView):

    def get(self, request, *args, **kwargs):
        html = biz.get_subscription_confirm_html(request, **kwargs)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        signature = request.POST.get('hid_signature', None)
        if not signature:
            return JsonResponse({'error': True, 'message': constants.ERROR_REQUEST_SIGNATURE})
        try:
            kwargs.update({'signature': signature})
            html = biz.get_subscription_confirm_html(request, **kwargs)
            task = get_object_or_404(Task, pk=kwargs.get('task_id')).get_next_task()
            data = biz.generate_report_pdf_binary(html)
            # 申込書確認のタスクに作成したＰＤＦファイルを追加する。
            for report in task.get_report_list():
                report.delete()
            content_file = ContentFile(data.getvalue(), name='subscription.pdf')
            report_file = models.ReportFile(content_object=task, name=constants.REPORT_SUBSCRIPTION_CONFIRM, path=content_file)
            report_file.save()
            return JsonResponse({'error': False, 'message': '成功しました。'})
        except Exception as ex:
            return JsonResponse({'error': True, 'message': str(ex)})


class SubscriptionView(BaseView):

    def get(self, request, *args, **kwargs):
        html = biz.get_subscription_html(request, **kwargs)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        report = get_object_or_404(models.ReportSubscription, pk=kwargs.get('report_id'))
        parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
        contractor = get_object_or_404(TempContractor, pk=kwargs.get('contractor_id'))
        return JsonResponse(dict())


class GenerateSubscriptionConfirmPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
        html = biz.get_subscription_confirm_html(request, **kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + parking_lot.name
        return response


class GenerateSubscriptionPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
        html = biz.get_subscription_html(request, **kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + parking_lot.name
        return response
