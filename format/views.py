import os
import datetime

from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from . import biz, models
from contract.models import Task
from parkinglot.models import ParkingLot
from utils import constants, common
from utils.django_base import BaseView, BaseTemplateView

logger = common.get_ap_logger()


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
        title, html = biz.get_subscription_confirm_html(request, **kwargs)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        signature = request.POST.get('hid_signature', None)
        if not signature and 'hid_signature' in request.POST:
            return JsonResponse({'error': True, 'message': constants.ERROR_REQUEST_SIGNATURE})
        try:
            kwargs.update({'signature': signature})
            title, html = biz.get_subscription_confirm_html(request, **kwargs)
            task = get_object_or_404(Task, pk=kwargs.get('task_id')).get_next_task()
            data = biz.generate_report_pdf_binary(html)
            # 申込書確認のタスクに作成したＰＤＦファイルを追加する。
            for report in task.reports.all():
                report.delete()
            content_file = ContentFile(data.getvalue(), name='subscription.pdf')
            report_file = models.ReportFile(content_object=task, name=constants.REPORT_SUBSCRIPTION_CONFIRM,
                                            path=content_file)
            report_file.save()
            return JsonResponse({'error': False, 'message': '成功しました。'})
        except Exception as ex:
            logger.error(ex)
            return JsonResponse({'error': True, 'message': str(ex)})


class SubscriptionView(BaseView):

    def get(self, request, *args, **kwargs):
        title, html = biz.get_subscription_html(request, **kwargs)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('task_id'))
        contractor = task.process.content_object.contractor
        contract = task.process.content_object
        # 車庫証明
        rdo_receipt = request.POST.get('rdo_receipt')
        # 駐車する車
        txt_car_maker = request.POST.get('txt_car_maker')
        txt_car_model = request.POST.get('txt_car_model')
        txt_no_plate = request.POST.get('txt_no_plate')
        txt_car_length = request.POST.get('txt_car_length')
        txt_car_width = request.POST.get('txt_car_width')
        txt_car_height = request.POST.get('txt_car_height')
        txt_car_weight = request.POST.get('txt_car_weight')
        # 希望契約開始日
        txt_contract_start_date = request.POST.get('txt_contract_start_date')
        # 希望契約期間
        rdo_contract_period = request.POST.get('rdo_contract_period')
        # 法人連絡先
        txt_corporate_kana = request.POST.get('txt_corporate_kana')
        txt_corporate_name = request.POST.get('txt_corporate_name')
        txt_corporate_president = request.POST.get('txt_corporate_president')
        txt_corporate_post1 = request.POST.get('txt_corporate_post1')
        txt_corporate_post2 = request.POST.get('txt_corporate_post2')
        txt_corporate_address1 = request.POST.get('txt_corporate_address1')
        txt_corporate_address2 = request.POST.get('txt_corporate_address2')
        txt_corporate_tel = request.POST.get('txt_corporate_tel')
        txt_corporate_fax = request.POST.get('txt_corporate_fax')
        txt_corporate_business_type = request.POST.get('txt_corporate_business_type')
        # 法人（契約担当者）
        txt_corporate_staff_kana = request.POST.get('txt_corporate_staff_kana')
        txt_corporate_staff_name = request.POST.get('txt_corporate_staff_name')
        txt_corporate_staff_email = request.POST.get('txt_corporate_staff_email')
        txt_corporate_staff_tel = request.POST.get('txt_corporate_staff_tel')
        txt_corporate_staff_fax = request.POST.get('txt_corporate_staff_fax')
        txt_corporate_staff_phone = request.POST.get('txt_corporate_staff_phone')
        # 法人（緊急連絡先）
        txt_corporate_contact_tel = request.POST.get('txt_corporate_contact_tel')
        txt_corporate_contact_name = request.POST.get('txt_corporate_contact_name')
        txt_corporate_contact_relation = request.POST.get('txt_corporate_contact_relation')
        # 個人連絡先
        txt_personal_kana = request.POST.get('txt_personal_kana')
        txt_personal_name = request.POST.get('txt_personal_name')
        txt_personal_birthday = request.POST.get('txt_personal_birthday')
        txt_personal_post1 = request.POST.get('txt_personal_post1')
        txt_personal_post2 = request.POST.get('txt_personal_post2')
        txt_personal_address1 = request.POST.get('txt_personal_address1')
        txt_personal_address2 = request.POST.get('txt_personal_address2')
        txt_personal_tel = request.POST.get('txt_personal_tel')
        txt_personal_email = request.POST.get('txt_personal_email')
        # 個人（勤務先）
        txt_workplace_name = request.POST.get('txt_workplace_name')
        txt_workplace_address1 = request.POST.get('txt_workplace_address1')
        txt_workplace_address2 = request.POST.get('txt_workplace_address2')
        txt_workplace_tel = request.POST.get('txt_workplace_tel')
        txt_workplace_fax = request.POST.get('txt_workplace_fax')
        # 個人（緊急連絡先）
        txt_personal_contact_tel = request.POST.get('txt_personal_contact_tel')
        txt_personal_contact_name = request.POST.get('txt_personal_contact_name')
        txt_personal_contact_relation = request.POST.get('txt_personal_contact_relation')
        # 媒介
        chk_route_flier = request.POST.get('chk_route_flier')
        chk_route_internet = request.POST.get('chk_route_internet')
        chk_route_board = request.POST.get('chk_route_board')
        chk_route_news = request.POST.get('chk_route_news')
        chk_route_estate = request.POST.get('chk_route_estate')
        chk_route_introduced = request.POST.get('chk_route_introduced')
        chk_route_other = request.POST.get('chk_route_other')
        txt_route_other = request.POST.get('txt_route_other')
        # 順番待ち
        rdo_waiting = request.POST.get('rdo_waiting')

        return JsonResponse(dict())


class GenerateSubscriptionConfirmPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        title, html = biz.get_subscription_confirm_html(request, **kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + title
        return response


class GenerateSubscriptionPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        title, html = biz.get_subscription_html(request, **kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + title
        return response
