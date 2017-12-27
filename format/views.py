import datetime
import json

from django.core import signing
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect

from . import biz, models
from contract.models import Task, ContractorCar
from master.models import TransmissionRoute
from utils import constants, common
from utils.app_base import get_unsigned_value, get_total_context, push_notification
from utils.django_base import BaseView, BaseTemplateViewWithoutLogin

logger = common.get_ap_logger()


# Create your views here
class BaseUserOperationView(BaseTemplateViewWithoutLogin):

    def get_context_data(self, **kwargs):
        context = super(BaseUserOperationView, self).get_context_data(**kwargs)
        signature = kwargs.get('signature')
        task_id = get_unsigned_value(signature)
        task = get_object_or_404(Task, pk=task_id)

        # if 'steps' in request.session:
        #     steps = request.session['steps']
        # else:
        steps = self.get_steps(signature)
        self.request.session['steps'] = steps
        context.update({
            'task': task,
            'signature': signature,
            'steps': steps,
        })
        context.update(get_total_context())
        return context

    def get(self, request, *args, **kwargs):
        try:
            response = super(BaseUserOperationView, self).get(request, *args, **kwargs)
            return response
        except signing.BadSignature:
            return redirect('format:url_timeout')

    def get_steps(self, signature=None):
        pass


class BaseUserSubscriptionView(BaseUserOperationView):

    def get_context_data(self, **kwargs):
        context = super(BaseUserSubscriptionView, self).get_context_data(**kwargs)
        context.update({
            'user_subscription': self.get_user_subscription(),
        })
        return context

    def get_steps(self, signature=None):
        return biz.get_user_subscription_steps(signature)

    def get_user_subscription(self):
        """ユーザー申込み情報を取得する。

        :return:
        """
        if 'user_subscription' in self.request.session:
            user_subscription = json.loads(self.request.session['user_subscription'])
            return user_subscription
        else:
            user_subscription = {
                'car': dict(),
                'contract': dict(),
            }
            return user_subscription

    def set_user_subscription(self, user_subscription):
        """ユーザー申込み情報をセッションに保存する

        :param user_subscription:
        :return:
        """
        self.request.session['user_subscription'] = json.dumps(user_subscription, default=common.date_handler)


class UserSubscriptionStep1View(BaseUserSubscriptionView):
    template_name = 'format/user_subscription_step1.html'

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionStep1View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        task = context.get('task')
        contract = task.process.content_object
        parking_lot = contract.parking_lot
        parking_position = contract.parking_position
        transmission_routes = TransmissionRoute.objects.public_all()
        current_step = steps[0]
        context.update({
            'title': current_step.get('name'),
            'contract': contract,
            'parking_lot': parking_lot,
            'parking_position': parking_position,
            'current_step': current_step,
            'transmission_routes': transmission_routes,
        })
        return context

    def post(self, request, *args, **kwargs):
        kwargs.update({
            'request': request,
        })
        context = self.get_context_data(**kwargs)
        errors = dict()
        user_subscription = self.get_user_subscription()
        car = user_subscription.get('car')
        contract = user_subscription.get('contract')
        # 駐車する車
        txt_car_maker = request.POST.get('txt_car_maker') or None
        txt_car_model = request.POST.get('txt_car_model') or None
        txt_no_plate = request.POST.get('txt_no_plate') or None
        txt_car_length = request.POST.get('txt_car_length') or None
        txt_car_width = request.POST.get('txt_car_width') or None
        txt_car_height = request.POST.get('txt_car_height') or None
        txt_car_weight = request.POST.get('txt_car_weight') or None
        car['car_maker'] = txt_car_maker
        car['car_model'] = txt_car_model
        car['car_no_plate'] = txt_no_plate
        car['car_length'] = txt_car_length
        car['car_width'] = txt_car_width
        car['car_height'] = txt_car_height
        car['car_weight'] = txt_car_weight
        # 任意保険の加入
        rdo_insurance = request.POST.get('rdo_insurance')
        txt_insurance_limit_amount = request.POST.get('txt_insurance_limit_amount')
        txt_insurance_expiration = request.POST.get('txt_insurance_expiration')
        car['rdo_insurance'] = rdo_insurance
        car['insurance_limit_amount'] = txt_insurance_limit_amount
        car['insurance_expiration'] = txt_insurance_expiration
        # 希望契約開始日
        txt_contract_start_date = request.POST.get('txt_contract_start_date') or None
        contract['start_date'] = txt_contract_start_date
        # 希望契約期間
        rdo_contract_period = request.POST.get('rdo_contract_period')
        txt_contract_end_month = request.POST.get('txt_contract_end_month')
        contract['contract_period'] = rdo_contract_period
        contract['contract_end_month'] = txt_contract_end_month
        # 車庫証明
        rdo_receipt = request.POST.get('rdo_receipt')
        contract['rdo_receipt'] = rdo_receipt
        # 順番待ち
        rdo_waiting = request.POST.get('rdo_waiting')
        contract['rdo_waiting'] = rdo_waiting
        # アンケート
        user_subscription['transmission_routes'] = transmission_routes = []
        for route in context.get('transmission_routes'):
            name = 'chk_route_%s' % route.pk
            if request.POST.get(name) == 'on':
                transmission_routes.append(name)
        txt_route_other = request.POST.get('txt_route_other')
        user_subscription['transmission_other'] = txt_route_other

        if not errors:
            # ユーザーが記入した情報を一時的にセッションに保存
            self.set_user_subscription(user_subscription)
            signature = context.get('signature')
            current_step = context.get('current_step')
            current_step.update({'is_finished': True})
            return redirect('format:user_subscription_step2', signature=signature)
        else:
            context.update(errors)
            return self.render_to_response(context)


class UserSubscriptionStep2View(BaseUserSubscriptionView):
    template_name = 'format/user_subscription_step2.html'

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionStep2View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[1]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        signature = context.get('signature')
        contractor_category = request.POST.get('contractor_category')
        user_subscription = self.get_user_subscription()
        user_subscription['contractor_category'] = contractor_category
        self.set_user_subscription(user_subscription)
        if contractor_category == 'corporate':
            return redirect('format:user_subscription_step3', signature=signature)
        elif contractor_category == 'personal':
            return redirect('format:user_subscription_step3', signature=signature)
        else:
            context.update({
                'contractor_corporate': ['法人か個人かをご選択してください。']
            })
            return self.render_to_response(context)


class UserSubscriptionStep3View(BaseUserSubscriptionView):
    template_name = 'format/user_subscription_step3.html'

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionStep3View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        user_subscription = self.get_user_subscription()
        is_personal = user_subscription['contractor_category'] == 'personal'
        current_step = steps[2]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
            'is_personal': is_personal,
        })
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        is_personal = context.get('is_personal')
        contractor = dict()
        errors = dict()
        if is_personal:
            contractor['category'] = 1
            # 個人連絡先
            txt_personal_kana = request.POST.get('txt_personal_kana') or None
            txt_personal_name = request.POST.get('txt_personal_name') or None
            txt_personal_birthday = request.POST.get('txt_personal_birthday') or None
            txt_personal_post1 = request.POST.get('txt_personal_post1') or None
            txt_personal_post2 = request.POST.get('txt_personal_post2') or None
            txt_personal_address1 = request.POST.get('txt_personal_address1') or None
            txt_personal_address2 = request.POST.get('txt_personal_address2') or None
            txt_personal_tel = request.POST.get('txt_personal_tel') or None
            txt_personal_phone = request.POST.get('txt_personal_phone') or None
            txt_personal_email = request.POST.get('txt_personal_email') or None
            contractor['kana'] = txt_personal_kana
            contractor['name'] = txt_personal_name
            contractor['personal_birthday'] = txt_personal_birthday
            contractor['post_code1'] = txt_personal_post1
            contractor['post_code2'] = txt_personal_post2
            contractor['address1'] = txt_personal_address1
            contractor['address2'] = txt_personal_address2
            contractor['tel'] = txt_personal_tel
            contractor['personal_phone'] = txt_personal_phone
            contractor['email'] = txt_personal_email
            # 個人（勤務先）
            txt_workplace_name = request.POST.get('txt_workplace_name') or None
            txt_workplace_post1 = request.POST.get('txt_workplace_post1') or None
            txt_workplace_post2 = request.POST.get('txt_workplace_post2') or None
            txt_workplace_address1 = request.POST.get('txt_workplace_address1') or None
            txt_workplace_address2 = request.POST.get('txt_workplace_address2') or None
            txt_workplace_tel = request.POST.get('txt_workplace_tel') or None
            txt_workplace_fax = request.POST.get('txt_workplace_fax') or None
            txt_workplace_comment = request.POST.get('txt_workplace_comment') or None
            contractor['workplace_name'] = txt_workplace_name
            contractor['workplace_post_code1'] = txt_workplace_post1
            contractor['workplace_post_code2'] = txt_workplace_post2
            contractor['workplace_address1'] = txt_workplace_address1
            contractor['workplace_address2'] = txt_workplace_address2
            contractor['workplace_tel'] = txt_workplace_tel
            contractor['workplace_fax'] = txt_workplace_fax
            contractor['workplace_comment'] = txt_workplace_comment
            # 個人（緊急連絡先）
            txt_personal_contact_tel = request.POST.get('txt_personal_contact_tel') or None
            txt_personal_contact_name = request.POST.get('txt_personal_contact_name') or None
            txt_personal_contact_relation = request.POST.get('txt_personal_contact_relation') or None
            contractor['contact_name'] = txt_personal_contact_name
            contractor['contact_tel'] = txt_personal_contact_tel
            contractor['contact_relation'] = txt_personal_contact_relation
        else:
            contractor['category'] = 2
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
            contractor['kana'] = txt_corporate_kana
            contractor['name'] = txt_corporate_name
            contractor['corporate_president'] = txt_corporate_president
            contractor['post_code1'] = txt_corporate_post1
            contractor['post_code2'] = txt_corporate_post2
            contractor['address1'] = txt_corporate_address1
            contractor['address2'] = txt_corporate_address2
            contractor['tel'] = txt_corporate_tel
            contractor['fax'] = txt_corporate_fax
            contractor['corporate_business_type'] = txt_corporate_business_type
            # 法人（契約担当者）
            txt_corporate_staff_kana = request.POST.get('txt_corporate_staff_kana') or None
            txt_corporate_staff_name = request.POST.get('txt_corporate_staff_name') or None
            txt_corporate_staff_email = request.POST.get('txt_corporate_staff_email') or None
            txt_corporate_staff_tel = request.POST.get('txt_corporate_staff_tel') or None
            txt_corporate_staff_fax = request.POST.get('txt_corporate_staff_fax') or None
            txt_corporate_staff_phone = request.POST.get('txt_corporate_staff_phone') or None
            contractor['corporate_staff_kana'] = txt_corporate_staff_kana
            contractor['corporate_staff_name'] = txt_corporate_staff_name
            contractor['corporate_staff_email'] = txt_corporate_staff_email
            contractor['corporate_staff_tel'] = txt_corporate_staff_tel
            contractor['corporate_staff_fax'] = txt_corporate_staff_fax
            contractor['corporate_staff_phone'] = txt_corporate_staff_phone
            # 法人（緊急連絡先）
            txt_corporate_contact_tel = request.POST.get('txt_corporate_contact_tel') or None
            txt_corporate_contact_name = request.POST.get('txt_corporate_contact_name') or None
            txt_corporate_contact_relation = request.POST.get('txt_corporate_contact_relation') or None
            contractor['contact_name'] = txt_corporate_contact_name
            contractor['contact_tel'] = txt_corporate_contact_tel
            contractor['contact_relation'] = txt_corporate_contact_relation
            # 使用者・使用者所在地
            txt_corporate_user_kana = request.POST.get('txt_corporate_user_kana') or None
            txt_corporate_user_name = request.POST.get('txt_corporate_user_name') or None
            txt_corporate_user_tel = request.POST.get('txt_corporate_user_tel') or None
            txt_corporate_user_post1 = request.POST.get('txt_corporate_user_post1') or None
            txt_corporate_user_post2 = request.POST.get('txt_corporate_user_post2') or None
            txt_corporate_user_address1 = request.POST.get('txt_corporate_user_address1') or None
            contractor['corporate_user_kana'] = txt_corporate_user_kana
            contractor['corporate_user_name'] = txt_corporate_user_name
            contractor['corporate_user_tel'] = txt_corporate_user_tel
            contractor['corporate_user_post_code1'] = txt_corporate_user_post1
            contractor['corporate_user_post_code2'] = txt_corporate_user_post2
            contractor['corporate_user_address1'] = txt_corporate_user_address1
        if not errors:
            # ユーザーが記入した情報を一時的にセッションに保存
            user_subscription = self.get_user_subscription()
            user_subscription.update({
                'contractor': contractor,
            })
            self.set_user_subscription(user_subscription)
            signature = context.get('signature')
            current_step = context.get('current_step')
            current_step.update({'is_finished': True})
            return redirect('format:user_subscription_step4', signature=signature)
        else:
            context.update(errors)
            return self.render_to_response(context)


class UserSubscriptionStep4View(BaseUserSubscriptionView):
    template_name = 'format/user_subscription_step4.html'

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionStep4View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        task = context.get('task')
        contract = task.process.content_object
        parking_lot = contract.parking_lot
        parking_position = contract.parking_position
        current_step = steps[3]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
            'parking_lot': parking_lot,
            'parking_position': parking_position,
        })
        return context

    def post(self, request, *args, **kwargs):
        from django.contrib.auth.models import User
        push_notification(User.objects.filter(username='admin'), '申込み完了', '申込みは完了しました。')
        signature = kwargs.get('signature')
        return redirect('format:user_subscription_step5', signature=signature)


class UserSubscriptionStep5View(BaseUserSubscriptionView):
    template_name = 'format/user_subscription_step5.html'

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionStep5View, self).get_context_data(**kwargs)
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
        errors = {'error': False, 'message_list': message_list}
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
                errors.update({
                    'error': True,
                    'txt_contract_start_date': ['不正の日付が入力されています。']
                })
                message_list.append(str(ex))
        else:
            errors.update({
                'error': True,
                'txt_contract_start_date': ['希望契約開始日は必須項目です。']
            })
        # 希望契約期間
        rdo_contract_period = request.POST.get('rdo_contract_period')
        if rdo_contract_period:
            if rdo_contract_period == 'long':
                contract.end_date = contract.get_contract_end_date()
        else:
            errors.update({
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
                errors.update({
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
                errors.update({
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
            errors.update({
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

        if errors.get('error') is False:
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
                errors.update({'error': False, 'message': '成功しました。'})
            except Exception as ex:
                logger.error(ex)
                errors.update({'error': True, 'message': str(ex)})
        return JsonResponse(errors)


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


class UrlTimeoutView(BaseTemplateViewWithoutLogin):
    template_name = 'format/url_timeout.html'
