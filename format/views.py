import os
import datetime

from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from . import biz, models
from contract.models import Task, ContractorCar
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
            for report in task.reports.filter(name=constants.REPORT_SUBSCRIPTION_CONFIRM):
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
        task = get_object_or_404(Task, pk=kwargs.get('task_id')).get_next_task()
        contractor = task.process.content_object.contractor
        contract = task.process.content_object
        message_list = []
        json = {'error': False, 'message_list': message_list}
        # 車庫証明
        rdo_receipt = request.POST.get('rdo_receipt')
        # 駐車する車
        txt_car_maker = request.POST.get('txt_car_maker') or None
        txt_car_model = request.POST.get('txt_car_model') or None
        txt_no_plate = request.POST.get('txt_no_plate') or None
        txt_car_length = request.POST.get('txt_car_length') or None
        txt_car_width = request.POST.get('txt_car_width') or None
        txt_car_height = request.POST.get('txt_car_height') or None
        txt_car_weight = request.POST.get('txt_car_weight') or None
        if txt_car_maker or txt_car_model:
            car = ContractorCar(contractor=contractor, car_maker=txt_car_maker, car_model=txt_car_model)
            car.car_no_plate = txt_no_plate
            car.car_length = txt_car_length
            car.car_width = txt_car_width
            car.car_height = txt_car_height
            car.car_weight = txt_car_weight
        else:
            car = None
        # 希望契約開始日
        txt_contract_start_date = request.POST.get('txt_contract_start_date') or None
        if txt_contract_start_date:
            try:
                contract.start_date = datetime.datetime.strptime(txt_contract_start_date, '%Y-%m-%d').date()
            except Exception as ex:
                json.update({
                    'error': True,
                    'txt_contract_start_date': ['不正の日付が入力されています。']
                })
                message_list.append(str(ex))
        else:
            json.update({
                'error': True,
                'txt_contract_start_date': ['希望契約開始日は必須項目です。']
            })
        # 希望契約期間
        rdo_contract_period = request.POST.get('rdo_contract_period')
        if rdo_contract_period:
            if rdo_contract_period == 'long':
                contract.end_date = contract.get_contract_end_date()
        else:
            json.update({
                'error': True,
                'txt_contract_start_date': ['希望契約期間は必須項目です。']
            })
        rdo_contractor_type = request.POST.get('rdo_contractor_type')
        if rdo_contractor_type == '2':
            # 法人連絡先
            txt_corporate_kana = request.POST.get('txt_corporate_kana') or None
            txt_corporate_name = request.POST.get('txt_corporate_name') or None
            txt_corporate_president = request.POST.get('txt_corporate_president') or None
            txt_corporate_post1 = request.POST.get('txt_corporate_post1') or None
            txt_corporate_post2 = request.POST.get('txt_corporate_post2') or None
            txt_corporate_address1 = request.POST.get('txt_corporate_address1') or None
            txt_corporate_address2 = request.POST.get('txt_corporate_address2') or None
            txt_corporate_tel = request.POST.get('txt_corporate_tel') or None
            txt_corporate_fax = request.POST.get('txt_corporate_fax') or None
            txt_corporate_business_type = request.POST.get('txt_corporate_business_type') or None
            contractor.kana = txt_corporate_kana
            if txt_corporate_name:
                contractor.name = txt_corporate_name
            else:
                json.update({
                    'error': True,
                    'txt_corporate_name': ['法人名は必須項目です。']
                })
            contractor.corporate_president = txt_corporate_president
            if txt_corporate_post1 and txt_corporate_post2:
                contractor.post_code = '%s-%s' % (txt_corporate_post1, txt_corporate_post2)
            contractor.address1 = txt_corporate_address1
            contractor.address2 = txt_corporate_address2
            contractor.tel = txt_corporate_tel
            contractor.fax = txt_corporate_fax
            contractor.corporate_business_type = txt_corporate_business_type
            # 法人（契約担当者）
            txt_corporate_staff_kana = request.POST.get('txt_corporate_staff_kana') or None
            txt_corporate_staff_name = request.POST.get('txt_corporate_staff_name') or None
            txt_corporate_staff_email = request.POST.get('txt_corporate_staff_email') or None
            txt_corporate_staff_tel = request.POST.get('txt_corporate_staff_tel') or None
            txt_corporate_staff_fax = request.POST.get('txt_corporate_staff_fax') or None
            txt_corporate_staff_phone = request.POST.get('txt_corporate_staff_phone') or None
            contractor.corporate_staff_kana = txt_corporate_staff_kana
            contractor.corporate_staff_name = txt_corporate_staff_name
            contractor.email = txt_corporate_staff_email
            contractor.tel = txt_corporate_staff_tel
            contractor.fax = txt_corporate_staff_fax
            contractor.corporate_staff_phone = txt_corporate_staff_phone
            # 法人（緊急連絡先）
            txt_corporate_contact_tel = request.POST.get('txt_corporate_contact_tel') or None
            txt_corporate_contact_name = request.POST.get('txt_corporate_contact_name') or None
            txt_corporate_contact_relation = request.POST.get('txt_corporate_contact_relation') or None
            contractor.contact_name = txt_corporate_contact_name
            contractor.contact_tel = txt_corporate_contact_tel
            contractor.contact_relation = txt_corporate_contact_relation
        elif rdo_contractor_type == '1':
            # 個人連絡先
            txt_personal_kana = request.POST.get('txt_personal_kana') or None
            txt_personal_name = request.POST.get('txt_personal_name') or None
            txt_personal_birthday = request.POST.get('txt_personal_birthday') or None
            txt_personal_post1 = request.POST.get('txt_personal_post1') or None
            txt_personal_post2 = request.POST.get('txt_personal_post2') or None
            txt_personal_address1 = request.POST.get('txt_personal_address1') or None
            txt_personal_address2 = request.POST.get('txt_personal_address2') or None
            txt_personal_tel = request.POST.get('txt_personal_tel') or None
            txt_personal_email = request.POST.get('txt_personal_email') or None
            contractor.kana = txt_personal_kana
            if txt_personal_name:
                contractor.name = txt_personal_name
            else:
                json.update({
                    'error': True,
                    'txt_personal_name': ['氏名は必須項目です。']
                })
            contractor.personal_birthday = txt_personal_birthday
            if txt_personal_post1 and txt_personal_post2:
                contractor.post_code = '%s-%s' % (txt_personal_post1, txt_personal_post2)
            contractor.address1 = txt_personal_address1
            contractor.address2 = txt_personal_address2
            contractor.tel = txt_personal_tel
            contractor.email = txt_personal_email
            # 個人（勤務先）
            txt_workplace_name = request.POST.get('txt_workplace_name') or None
            txt_workplace_address1 = request.POST.get('txt_workplace_address1') or None
            txt_workplace_address2 = request.POST.get('txt_workplace_address2') or None
            txt_workplace_tel = request.POST.get('txt_workplace_tel') or None
            txt_workplace_fax = request.POST.get('txt_workplace_fax') or None
            contractor.workplace_name = txt_workplace_name
            contractor.workplace_address1 = txt_workplace_address1
            contractor.workplace_address2 = txt_workplace_address2
            contractor.workplace_tel = txt_workplace_tel
            contractor.workplace_fax = txt_workplace_fax
            # 個人（緊急連絡先）
            txt_personal_contact_tel = request.POST.get('txt_personal_contact_tel') or None
            txt_personal_contact_name = request.POST.get('txt_personal_contact_name') or None
            txt_personal_contact_relation = request.POST.get('txt_personal_contact_relation') or None
            contractor.contact_name = txt_personal_contact_name
            contractor.contact_tel = txt_personal_contact_tel
            contractor.contact_relation = txt_personal_contact_relation
        else:
            json.update({
                'error': True,
                'rdo_contractor_type': ['法人か個人か選択してください。']
            })
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
        if rdo_waiting == 'yes':
            pass
        elif rdo_waiting == 'no':
            pass

        if json.get('error') is False:
            try:
                if car:
                    car.save()
                    contract.car = car
                contract.save()
                contractor.save()
                # PDF作成
                kwargs.update({'contractor': contractor, 'contract': contract})
                title, html = biz.get_subscription_html(request, **kwargs)
                data = biz.generate_report_pdf_binary(html)
                # 申込書確認のタスクに作成したＰＤＦファイルを追加する。
                for report in task.reports.filter(name=constants.REPORT_SUBSCRIPTION):
                    report.delete()
                content_file = ContentFile(data.getvalue(), name='subscription.pdf')
                report_file = models.ReportFile(content_object=task, name=constants.REPORT_SUBSCRIPTION,
                                                path=content_file)
                report_file.save()
                json.update({'error': False, 'message': '成功しました。'})
            except Exception as ex:
                logger.error(ex)
                json.update({'error': True, 'message': str(ex)})
        return JsonResponse(json)


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
