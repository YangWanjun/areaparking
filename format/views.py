from django.contrib.auth.models import User
from django.contrib import messages
from django.core import signing
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.utils import timezone

from . import biz
from contract.serializers import SubscriptionSerializer, ContractCancellationSerializer
from contract.models import Contract, Subscription, ContractCancellation, Contractor
from parkinglot.models import ParkingLot, ParkingPosition
from utils import common, constants
from utils.app_base import get_unsigned_value, get_total_context, push_notification
from utils.django_base import BaseView, BaseTemplateViewWithoutLogin
from utils.errors import OperationFinishedException

logger = common.get_ap_logger()


# Create your views here
class BaseUserOperationView(BaseTemplateViewWithoutLogin):
    # ステップ完了後のＵＲＬ
    finished_url = None
    is_last_step = False

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(BaseUserOperationView, self).dispatch(request, *args, **kwargs)
        except signing.BadSignature:
            return redirect('format:url_timeout')
        except OperationFinishedException:
            if self.finished_url:
                return redirect(self.finished_url)

    def get_context_data(self, **kwargs):
        context = super(BaseUserOperationView, self).get_context_data(**kwargs)
        signature = kwargs.get('signature')
        pk = get_unsigned_value(signature)
        context.update({
            'pk': pk,
            'signature': signature,         # デジタル署名
            'is_finished': False,
            'is_all_active': False,
        })
        context.update(get_total_context())
        return context


class BaseUserSubscriptionView(BaseUserOperationView):

    def get_context_data(self, **kwargs):
        context = super(BaseUserSubscriptionView, self).get_context_data(**kwargs)
        signature = context.get('signature')
        steps = self.get_steps(signature)
        # 申込み対象（Subscription）の主キー
        pk = context.get('pk')
        user_subscription = self.get_user_subscription(pk)
        context.update({
            'user_subscription': user_subscription,
            'parking_lot': user_subscription.parking_lot,
            'steps': steps,
        })
        return context

    def get_steps(self, signature=None):
        pass

    def get_session_key(self):
        signature = self.kwargs.get('signature')
        pk = get_unsigned_value(signature)
        return 'user_subscription_%s' % pk

    def get_user_subscription(self, subscription_id):
        """ユーザー申込み情報を取得する。

        :return:
        """
        subscription = get_object_or_404(Subscription, pk=subscription_id)
        if self.is_subscription_finished(subscription):
            self.clear_session()
            # 既に入力済みであれば、終了する
            raise OperationFinishedException()
        if self.is_last_step:
            # 最後ステップの場合セッションをクリアする
            self.clear_session()
            return subscription
        elif self.get_session_key() in self.request.session:
            data = self.request.session[self.get_session_key()]
            return Subscription(**data)
        else:
            data = self.set_user_subscription(subscription)
            return Subscription(**data)

    def set_user_subscription(self, user_subscription):
        """ユーザー申込み情報をセッションに保存する

        :param user_subscription:
        :return:
        """
        serializer = SubscriptionSerializer(user_subscription)
        self.request.session[self.get_session_key()] = serializer.data
        return serializer.data

    def is_subscription_finished(self, subscription):
        pass

    def clear_session(self):
        """セッションに保存されているユーザー申込み情報をクリアする。

        :return:
        """
        if self.get_session_key() in self.request.session:
            del self.request.session[self.get_session_key()]


class BaseUserSubscriptionSimpleView(BaseUserSubscriptionView):

    def get_steps(self, signature=None):
        """申込み用フォーム(車室の一時確保に必要な項目)のステップ数

        :param signature:
        :return:
        """
        steps = biz.get_user_subscription_simple_steps(signature)
        # ステップ完了後のＵＲＬ
        self.finished_url = steps[-1].get('url', None)
        return steps


class UserSubscriptionSimpleStep1View(BaseUserSubscriptionSimpleView):
    template_name = 'format/user_subscription_simple_step1.html'

    def is_subscription_finished(self, subscription):
        """申込フォーム入力は完了したかどうか

        :param subscription:
        :return:
        """
        if subscription and subscription.status >= '03':
            # 申込フォーム入力完了
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionSimpleStep1View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[0]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_subscription = context.get('user_subscription')
        current_step = context.get('current_step')
        parking_lot = context.get('parking_lot')
        # 契約者分類
        contractor_category = request.POST.get('contractor_category')
        user_subscription.category = contractor_category
        if not contractor_category:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "契約者分類")
        # お名前
        name = request.POST.get('name') or None
        user_subscription.name = name
        if not name:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "お名前")
        # フリガナ
        kana = request.POST.get('kana') or None
        user_subscription.kana = kana
        if not kana:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "フリガナ")
        # 電話番号
        tel = request.POST.get('tel') or None
        user_subscription.tel = tel
        if not tel:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "電話番号")
        # メールアドレス
        email = request.POST.get('email') or None
        email_confirm = request.POST.get('email_confirm') or None
        user_subscription.email = email
        user_subscription.email_confirm = email_confirm
        if not email:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "メールアドレス")
        if not email_confirm:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "メールアドレス（確認）")
        # ご契約予定車両の車種
        car_model = request.POST.get('car_model') or None
        user_subscription.car_model = car_model
        if not car_model:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "ご契約予定車両の車種")
        # 希望契約開始日
        rdo_contract_start_date = request.POST.get('rdo_contract_start_date') or None
        if rdo_contract_start_date == "shortest":
            user_subscription.is_contract_start_shortest = True
        elif rdo_contract_start_date == "calendar":
            user_subscription.is_contract_start_shortest = False
            contract_start_date = request.POST.get('contract_start_date') or None
            user_subscription.contract_start_date = contract_start_date
        if not rdo_contract_start_date:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "希望契約開始日")
        # 保険加入の状況
        rdo_insurance = request.POST.get('rdo_insurance') or None
        user_subscription.insurance_join_status = rdo_insurance
        if not rdo_insurance:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "保険加入の状況")
        # 空き待ち
        rdo_waiting = request.POST.get('rdo_waiting') or None
        user_subscription.require_waiting = rdo_waiting
        if not rdo_waiting:
            messages.add_message(request, messages.ERROR, constants.ERROR_REQUIRED_FIELD % "空き待ち")
        # 備考
        comment = request.POST.get('comment') or None
        user_subscription.comment = comment
        # 承諾チェックボックス
        chk_agreement = request.POST.get('chk_agreement') or None
        if chk_agreement != 'on':
            messages.add_message(request, messages.ERROR, constants.ERROR_SUBSCRIPTION_PRIVACY_AGREEMENT)
        if email == email_confirm:
            user_subscription.email = email
            # 申込フォーム入力完了
            user_subscription.status = '03'
            user_subscription.simple_form_completed_date = timezone.now()
            user_subscription.save()
            self.set_user_subscription(user_subscription)
            # 通知（メールとプッシュ）
            push_notification(
                '%s 申込み完了' % str(parking_lot),
                '',
                url=reverse('contract:subscription_detail', args=(user_subscription.pk,)),
            )
            # セッションに保存された一時情報を削除する。
            self.clear_session()
            return redirect(current_step.get('next_step').get('url'))
        else:
            messages.add_message(request, messages.ERROR, constants.ERROR_SUBSCRIPTION_EMAIL_CONFIRM)

        return self.render_to_response(context)


class UserSubscriptionSimpleStep2View(BaseUserSubscriptionSimpleView):
    template_name = 'format/user_subscription_simple_step2.html'
    is_last_step = True

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionSimpleStep2View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[1]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
            'is_finished': True
        })
        return context


class BaseUserSubscriptionInspectionView(BaseUserSubscriptionView):

    def get_steps(self, signature=None):
        """審査用フォームのステップ数

        :param signature:
        :return:
        """
        steps = biz.get_user_subscription_inspection_steps(signature)
        # ステップ完了後のＵＲＬ
        self.finished_url = steps[-1].get('url', None)
        return steps


class UserSubscriptionInspectionStep1View(BaseUserSubscriptionInspectionView):
    template_name = 'format/user_subscription_inspection_step1.html'

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionInspectionStep1View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[0]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_subscription = context.get('user_subscription')
        current_step = context.get('current_step')
        parking_lot = context.get('parking_lot')
        push_notification(
            '%s 審査フォーム入力完了' % str(parking_lot),
            '',
            url=reverse('contract:subscription_detail', args=(user_subscription.pk,)),
        )
        return redirect(current_step.get('next_step').get('url'))


class UserSubscriptionInspectionStep2View(BaseUserSubscriptionInspectionView):
    template_name = 'format/user_subscription_inspection_step2.html'
    is_last_step = True

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionInspectionStep2View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[1]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
            'is_finished': True
        })
        return context


# class BaseUserSubscriptionView(BaseUserOperationView):
#
#     def get(self, request, *args, **kwargs):
#         try:
#             context = self.get_context_data(**kwargs)
#             # ステータスが「新規申込み」でない場合は申込み完了に飛ばす
#             subscription = get_object_or_404(Subscription, pk=context.get('pk'))
#             if subscription.status != '01' and context.get('is_finished') is False:
#                 return redirect('format:user_subscription_step5', signature=kwargs.get('signature'))
#             return self.render_to_response(context)
#         except signing.BadSignature:
#             return redirect('format:url_timeout')
#
#     def get_context_data(self, **kwargs):
#         context = super(BaseUserSubscriptionView, self).get_context_data(**kwargs)
#         signature = context.get('signature')
#         steps = self.get_steps(signature)
#         self.request.session['steps'] = steps
#         user_subscription = self.get_user_subscription(context.get('pk'))
#         context.update({
#             'user_subscription': user_subscription,
#             'parking_lot': user_subscription.parking_lot,
#             'steps': steps,
#         })
#         return context
#
#     def get_steps(self, signature=None):
#         return biz.get_user_subscription_steps(signature)
#
#     def get_user_subscription(self, subscription_id):
#         """ユーザー申込み情報を取得する。
#
#         :return:
#         """
#         subscription = get_object_or_404(Subscription, pk=subscription_id)
#         if 'user_subscription' in self.request.session:
#             data = self.request.session['user_subscription']
#             if str(data.get('code', 0)) != str(subscription_id):
#                 data = self.set_user_subscription(subscription)
#         else:
#             data = self.set_user_subscription(subscription)
#         return Subscription(**data)
#
#     def set_user_subscription(self, user_subscription):
#         """ユーザー申込み情報をセッションに保存する
#
#         :param user_subscription:
#         :return:
#         """
#         serializer = SubscriptionSerializer(user_subscription)
#         self.request.session['user_subscription'] = serializer.data
#         return serializer.data
#
#
# class UserSubscriptionStep1View(BaseUserSubscriptionView):
#     template_name = 'format/user_subscription_step1.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserSubscriptionStep1View, self).get_context_data(**kwargs)
#         steps = context.get('steps')
#         transmission_routes = TransmissionRoute.objects.public_all()
#         current_step = steps[0]
#         context.update({
#             'title': current_step.get('name'),
#             'current_step': current_step,
#             'transmission_routes': transmission_routes,
#         })
#         return context
#
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         user_subscription = context.get('user_subscription')
#         errors = dict()
#         # 駐車する車
#         txt_car_maker = request.POST.get('txt_car_maker') or None
#         txt_car_model = request.POST.get('txt_car_model') or None
#         txt_no_plate = request.POST.get('txt_no_plate') or None
#         txt_car_length = request.POST.get('txt_car_length') or None
#         txt_car_width = request.POST.get('txt_car_width') or None
#         txt_car_height = request.POST.get('txt_car_height') or None
#         txt_car_weight = request.POST.get('txt_car_weight') or None
#         user_subscription.car_maker = txt_car_maker
#         user_subscription.car_model = txt_car_model
#         user_subscription.car_no_plate = txt_no_plate
#         user_subscription.car_length = txt_car_length
#         user_subscription.car_width = txt_car_width
#         user_subscription.car_height = txt_car_height
#         user_subscription.car_weight = txt_car_weight
#         # 任意保険の加入
#         rdo_insurance = request.POST.get('rdo_insurance') or None
#         txt_insurance_limit_amount = request.POST.get('txt_insurance_limit_amount') or None
#         txt_insurance_expiration = request.POST.get('txt_insurance_expiration') or None
#         user_subscription.insurance_join_status = rdo_insurance
#         user_subscription.insurance_limit_amount = txt_insurance_limit_amount
#         user_subscription.insurance_expire_date = txt_insurance_expiration
#         # 希望契約開始日
#         txt_contract_start_date = request.POST.get('txt_contract_start_date') or None
#         user_subscription.contract_start_date = txt_contract_start_date
#         # 希望契約期間
#         rdo_contract_period = request.POST.get('rdo_contract_period') or None
#         txt_contract_end_month = request.POST.get('txt_contract_end_month') or None
#         user_subscription.contract_period = rdo_contract_period
#         user_subscription.contract_end_month = txt_contract_end_month
#         # 車庫証明
#         rdo_receipt = request.POST.get('rdo_receipt') or None
#         user_subscription.require_receipt = rdo_receipt
#         # 順番待ち
#         rdo_waiting = request.POST.get('rdo_waiting') or None
#         user_subscription.require_waiting = rdo_waiting
#         # アンケート
#         transmission_routes = []
#         for route in context.get('transmission_routes'):
#             name = 'chk_route_%s' % route.pk
#             if request.POST.get(name) is not None:
#                 transmission_routes.append(request.POST.get(name))
#         if transmission_routes:
#             user_subscription.transmission_routes = ','.join(transmission_routes)
#         txt_route_other = request.POST.get('txt_route_other') or None
#         user_subscription.transmission_other_route = txt_route_other
#
#         if not errors:
#             # ユーザーが記入した情報を一時的にセッションに保存
#             self.set_user_subscription(user_subscription)
#             signature = context.get('signature')
#             current_step = context.get('current_step')
#             current_step.update({'is_finished': True})
#             return redirect('format:user_subscription_step2', signature=signature)
#         else:
#             context.update(errors)
#             return self.render_to_response(context)
#
#
# class UserSubscriptionStep2View(BaseUserSubscriptionView):
#     template_name = 'format/user_subscription_step2.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserSubscriptionStep2View, self).get_context_data(**kwargs)
#         steps = context.get('steps')
#         current_step = steps[1]
#         context.update({
#             'title': current_step.get('name'),
#             'current_step': current_step,
#         })
#         return context
#
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         signature = context.get('signature')
#         contractor_category = request.POST.get('contractor_category')
#         user_subscription = context.get('user_subscription')
#         user_subscription.category = contractor_category
#         self.set_user_subscription(user_subscription)
#         if contractor_category == '2':
#             return redirect('format:user_subscription_step3', signature=signature)
#         elif contractor_category == '1':
#             return redirect('format:user_subscription_step3', signature=signature)
#         else:
#             context.update({
#                 'contractor_corporate': ['法人か個人かをご選択してください。']
#             })
#             return self.render_to_response(context)
#
#
# class UserSubscriptionStep3View(BaseUserSubscriptionView):
#     template_name = 'format/user_subscription_step3.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserSubscriptionStep3View, self).get_context_data(**kwargs)
#         steps = context.get('steps')
#         current_step = steps[2]
#         context.update({
#             'title': current_step.get('name'),
#             'current_step': current_step,
#         })
#         return context
#
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         user_subscription = context.get('user_subscription')
#         errors = dict()
#         if user_subscription.category == '1':
#             # 個人連絡先
#             txt_personal_kana = request.POST.get('txt_personal_kana') or None
#             txt_personal_name = request.POST.get('txt_personal_name') or None
#             txt_personal_birthday = request.POST.get('txt_personal_birthday') or None
#             txt_personal_post_code1 = request.POST.get('txt_personal_post1') or None
#             txt_personal_post_code2 = request.POST.get('txt_personal_post2') or None
#             txt_personal_address1 = request.POST.get('txt_personal_address1') or None
#             txt_personal_address2 = request.POST.get('txt_personal_address2') or None
#             txt_personal_tel = request.POST.get('txt_personal_tel') or None
#             txt_personal_phone = request.POST.get('txt_personal_phone') or None
#             txt_personal_email = request.POST.get('txt_personal_email') or None
#             user_subscription.kana = txt_personal_kana
#             user_subscription.name = txt_personal_name
#             user_subscription.personal_birthday = txt_personal_birthday
#             user_subscription.post_code1 = txt_personal_post_code1
#             user_subscription.post_code2 = txt_personal_post_code2
#             user_subscription.address1 = txt_personal_address1
#             user_subscription.address2 = txt_personal_address2
#             user_subscription.tel = txt_personal_tel
#             user_subscription.personal_phone = txt_personal_phone
#             user_subscription.email = txt_personal_email
#             # 個人（勤務先）
#             txt_workplace_name = request.POST.get('txt_workplace_name') or None
#             txt_workplace_post1 = request.POST.get('txt_workplace_post1') or None
#             txt_workplace_post2 = request.POST.get('txt_workplace_post2') or None
#             txt_workplace_address1 = request.POST.get('txt_workplace_address1') or None
#             txt_workplace_address2 = request.POST.get('txt_workplace_address2') or None
#             txt_workplace_tel = request.POST.get('txt_workplace_tel') or None
#             txt_workplace_fax = request.POST.get('txt_workplace_fax') or None
#             txt_workplace_comment = request.POST.get('txt_workplace_comment') or None
#             user_subscription.workplace_name = txt_workplace_name
#             user_subscription.workplace_post_code1 = txt_workplace_post1
#             user_subscription.workplace_post_code2 = txt_workplace_post2
#             user_subscription.workplace_address1 = txt_workplace_address1
#             user_subscription.workplace_address2 = txt_workplace_address2
#             user_subscription.workplace_tel = txt_workplace_tel
#             user_subscription.workplace_fax = txt_workplace_fax
#             user_subscription.workplace_comment = txt_workplace_comment
#             # 個人（緊急連絡先）
#             txt_personal_contact_tel = request.POST.get('txt_personal_contact_tel') or None
#             txt_personal_contact_name = request.POST.get('txt_personal_contact_name') or None
#             txt_personal_contact_relation = request.POST.get('txt_personal_contact_relation') or None
#             user_subscription.contact_name = txt_personal_contact_name
#             user_subscription.contact_tel = txt_personal_contact_tel
#             user_subscription.contact_relation = txt_personal_contact_relation
#         else:
#             # 法人連絡先
#             txt_corporate_kana = request.POST.get('txt_corporate_kana') or None
#             txt_corporate_name = request.POST.get('txt_corporate_name') or None
#             txt_corporate_president = request.POST.get('txt_corporate_president') or None
#             txt_corporate_post1 = request.POST.get('txt_corporate_post1') or None
#             txt_corporate_post2 = request.POST.get('txt_corporate_post2') or None
#             txt_corporate_address1 = request.POST.get('txt_corporate_address1') or None
#             txt_corporate_address2 = request.POST.get('txt_corporate_address2') or None
#             txt_corporate_tel = request.POST.get('txt_corporate_tel') or None
#             txt_corporate_fax = request.POST.get('txt_corporate_fax') or None
#             txt_corporate_business_type = request.POST.get('txt_corporate_business_type') or None
#             user_subscription.kana = txt_corporate_kana
#             user_subscription.name = txt_corporate_name
#             user_subscription.corporate_president = txt_corporate_president
#             user_subscription.post_code1 = txt_corporate_post1
#             user_subscription.post_code2 = txt_corporate_post2
#             user_subscription.address1 = txt_corporate_address1
#             user_subscription.address2 = txt_corporate_address2
#             user_subscription.tel = txt_corporate_tel
#             user_subscription.fax = txt_corporate_fax
#             user_subscription.corporate_business_type = txt_corporate_business_type
#             # 法人（契約担当者）
#             txt_corporate_staff_kana = request.POST.get('txt_corporate_staff_kana') or None
#             txt_corporate_staff_name = request.POST.get('txt_corporate_staff_name') or None
#             txt_corporate_staff_email = request.POST.get('txt_corporate_staff_email') or None
#             txt_corporate_staff_tel = request.POST.get('txt_corporate_staff_tel') or None
#             txt_corporate_staff_fax = request.POST.get('txt_corporate_staff_fax') or None
#             txt_corporate_staff_phone = request.POST.get('txt_corporate_staff_phone') or None
#             user_subscription.corporate_staff_kana = txt_corporate_staff_kana
#             user_subscription.corporate_staff_name = txt_corporate_staff_name
#             user_subscription.corporate_staff_email = txt_corporate_staff_email
#             user_subscription.corporate_staff_tel = txt_corporate_staff_tel
#             user_subscription.corporate_staff_fax = txt_corporate_staff_fax
#             user_subscription.corporate_staff_phone = txt_corporate_staff_phone
#             # 法人（緊急連絡先）
#             txt_corporate_contact_tel = request.POST.get('txt_corporate_contact_tel') or None
#             txt_corporate_contact_name = request.POST.get('txt_corporate_contact_name') or None
#             txt_corporate_contact_relation = request.POST.get('txt_corporate_contact_relation') or None
#             user_subscription.contact_name = txt_corporate_contact_name
#             user_subscription.contact_tel = txt_corporate_contact_tel
#             user_subscription.contact_relation = txt_corporate_contact_relation
#             # 使用者・使用者所在地
#             txt_corporate_user_kana = request.POST.get('txt_corporate_user_kana') or None
#             txt_corporate_user_name = request.POST.get('txt_corporate_user_name') or None
#             txt_corporate_user_tel = request.POST.get('txt_corporate_user_tel') or None
#             txt_corporate_user_post1 = request.POST.get('txt_corporate_user_post1') or None
#             txt_corporate_user_post2 = request.POST.get('txt_corporate_user_post2') or None
#             txt_corporate_user_address1 = request.POST.get('txt_corporate_user_address1') or None
#             user_subscription.corporate_user_kana = txt_corporate_user_kana
#             user_subscription.corporate_user_name = txt_corporate_user_name
#             user_subscription.corporate_user_tel = txt_corporate_user_tel
#             user_subscription.corporate_user_post_code1 = txt_corporate_user_post1
#             user_subscription.corporate_user_post_code2 = txt_corporate_user_post2
#             user_subscription.corporate_user_address1 = txt_corporate_user_address1
#         if not errors:
#             # ユーザーが記入した情報を一時的にセッションに保存
#             self.set_user_subscription(user_subscription)
#             signature = context.get('signature')
#             return redirect('format:user_subscription_step4', signature=signature)
#         else:
#             context.update(errors)
#             return self.render_to_response(context)
#
#
# class UserSubscriptionStep4View(BaseUserSubscriptionView):
#     template_name = 'format/user_subscription_step4.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserSubscriptionStep4View, self).get_context_data(**kwargs)
#         steps = context.get('steps')
#         current_step = steps[3]
#         context.update({
#             'title': current_step.get('name'),
#             'current_step': current_step,
#         })
#         return context
#
#     def post(self, request, *args, **kwargs):
#         context = super(UserSubscriptionStep4View, self).get_context_data(**kwargs)
#         user_subscription = context.get('user_subscription')
#         # 申込PDF作成
#         biz.generate_subscription_pdf(request, user_subscription, **kwargs)
#         # 申込みデータをＤＢに保存
#         user_subscription.status = '02'     # 申込み完了
#         user_subscription.save()
#         self.set_user_subscription(user_subscription)
#         # 通知（メールとプッシュ）
#         parking_lot = context.get('parking_lot')
#         mail_group = MailGroup.get_subscription_completed_group()
#         data = user_subscription.get_subscription_addressee()
#         mail_group.send_main(user_subscription.get_subscription_email(), data)
#         push_notification(
#             None,
#             '%s 申込み完了' % str(parking_lot),
#             '',
#             url=reverse('contract:subscription_detail', args=(user_subscription.pk,)),
#         )
#         signature = kwargs.get('signature')
#         return redirect('format:user_subscription_step5', signature=signature)
#
#
# class UserSubscriptionStep5View(BaseUserSubscriptionView):
#     template_name = 'format/user_subscription_step5.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserSubscriptionStep5View, self).get_context_data(**kwargs)
#         steps = context.get('steps')
#         current_step = steps[4]
#         context.update({
#             'title': current_step.get('name'),
#             'current_step': current_step,
#             'is_finished': True
#         })
#         return context


class SubscriptionConfirmView(BaseView):

    def get(self, request, *args, **kwargs):
        subscription = get_object_or_404(Subscription, pk=kwargs.get('subscription_id'))
        title, html = biz.get_subscription_confirm_html(request, subscription, **kwargs)
        return HttpResponse(html)

    # def post(self, request, *args, **kwargs):
    #     signature = request.POST.get('hid_signature', None)
    #     if not signature and 'hid_signature' in request.POST:
    #         return JsonResponse({'error': True, 'message': constants.ERROR_REQUEST_SIGNATURE})
    #     try:
    #         kwargs.update({'signature': signature})
    #         title, html = biz.get_subscription_confirm_html(request, **kwargs)
    #         task = get_object_or_404(Task, pk=kwargs.get('task_id')).get_next_task()
    #         data = biz.generate_report_pdf_binary(html)
    #         # 申込書確認のタスクに作成したＰＤＦファイルを追加する。
    #         for report in task.reports.filter(name=constants.REPORT_SUBSCRIPTION_CONFIRM):
    #             report.delete()
    #         content_file = ContentFile(data.getvalue(), name='subscription.pdf')
    #         report_file = models.ReportFile(content_object=task, name=constants.REPORT_SUBSCRIPTION_CONFIRM,
    #                                         path=content_file)
    #         report_file.save()
    #         return JsonResponse({'error': False, 'message': '成功しました。'})
    #     except Exception as ex:
    #         logger.error(ex)
    #         return JsonResponse({'error': True, 'message': str(ex)})


class SubscriptionView(BaseView):

    def get(self, request, *args, **kwargs):
        subscription = get_object_or_404(Subscription, pk=kwargs.get('subscription_id'))
        title, html = biz.get_subscription_html(request, subscription, **kwargs)
        return HttpResponse(html)

    # def post(self, request, *args, **kwargs):
    #     task = get_object_or_404(Task, pk=kwargs.get('task_id')).get_next_task()
    #     contractor = task.process.content_object.contractor
    #     contract = task.process.content_object
    #     message_list = []
    #     errors = {'error': False, 'message_list': message_list}
    #     # 車庫証明
    #     rdo_receipt = request.POST.get('rdo_receipt')
    #     # 駐車する車
    #     txt_car_maker = request.POST.get('txt_car_maker') or None
    #     txt_car_model = request.POST.get('txt_car_model') or None
    #     txt_no_plate = request.POST.get('txt_no_plate') or None
    #     txt_car_length = request.POST.get('txt_car_length') or None
    #     txt_car_width = request.POST.get('txt_car_width') or None
    #     txt_car_height = request.POST.get('txt_car_height') or None
    #     txt_car_weight = request.POST.get('txt_car_weight') or None
    #     if txt_car_maker or txt_car_model:
    #         car = ContractorCar(contractor=contractor, car_maker=txt_car_maker, car_model=txt_car_model)
    #         car.car_no_plate = txt_no_plate
    #         car.car_length = txt_car_length
    #         car.car_width = txt_car_width
    #         car.car_height = txt_car_height
    #         car.car_weight = txt_car_weight
    #     else:
    #         car = None
    #     # 希望契約開始日
    #     txt_contract_start_date = request.POST.get('txt_contract_start_date') or None
    #     if txt_contract_start_date:
    #         try:
    #             contract.start_date = datetime.datetime.strptime(txt_contract_start_date, '%Y-%m-%d').date()
    #         except Exception as ex:
    #             errors.update({
    #                 'error': True,
    #                 'txt_contract_start_date': ['不正の日付が入力されています。']
    #             })
    #             message_list.append(str(ex))
    #     else:
    #         errors.update({
    #             'error': True,
    #             'txt_contract_start_date': ['希望契約開始日は必須項目です。']
    #         })
    #     # 希望契約期間
    #     rdo_contract_period = request.POST.get('rdo_contract_period')
    #     if rdo_contract_period:
    #         if rdo_contract_period == 'long':
    #             contract.end_date = contract.get_contract_end_date()
    #     else:
    #         errors.update({
    #             'error': True,
    #             'txt_contract_start_date': ['希望契約期間は必須項目です。']
    #         })
    #     rdo_contractor_type = request.POST.get('rdo_contractor_type')
    #     if rdo_contractor_type == '2':
    #         # 法人連絡先
    #         txt_corporate_kana = request.POST.get('txt_corporate_kana') or None
    #         txt_corporate_name = request.POST.get('txt_corporate_name') or None
    #         txt_corporate_president = request.POST.get('txt_corporate_president') or None
    #         txt_corporate_post1 = request.POST.get('txt_corporate_post1') or None
    #         txt_corporate_post2 = request.POST.get('txt_corporate_post2') or None
    #         txt_corporate_address1 = request.POST.get('txt_corporate_address1') or None
    #         txt_corporate_address2 = request.POST.get('txt_corporate_address2') or None
    #         txt_corporate_tel = request.POST.get('txt_corporate_tel') or None
    #         txt_corporate_fax = request.POST.get('txt_corporate_fax') or None
    #         txt_corporate_business_type = request.POST.get('txt_corporate_business_type') or None
    #         contractor.kana = txt_corporate_kana
    #         if txt_corporate_name:
    #             contractor.name = txt_corporate_name
    #         else:
    #             errors.update({
    #                 'error': True,
    #                 'txt_corporate_name': ['法人名は必須項目です。']
    #             })
    #         contractor.corporate_president = txt_corporate_president
    #         if txt_corporate_post1 and txt_corporate_post2:
    #             contractor.post_code = '%s-%s' % (txt_corporate_post1, txt_corporate_post2)
    #         contractor.address1 = txt_corporate_address1
    #         contractor.address2 = txt_corporate_address2
    #         contractor.tel = txt_corporate_tel
    #         contractor.fax = txt_corporate_fax
    #         contractor.corporate_business_type = txt_corporate_business_type
    #         # 法人（契約担当者）
    #         txt_corporate_staff_kana = request.POST.get('txt_corporate_staff_kana') or None
    #         txt_corporate_staff_name = request.POST.get('txt_corporate_staff_name') or None
    #         txt_corporate_staff_email = request.POST.get('txt_corporate_staff_email') or None
    #         txt_corporate_staff_tel = request.POST.get('txt_corporate_staff_tel') or None
    #         txt_corporate_staff_fax = request.POST.get('txt_corporate_staff_fax') or None
    #         txt_corporate_staff_phone = request.POST.get('txt_corporate_staff_phone') or None
    #         contractor.corporate_staff_kana = txt_corporate_staff_kana
    #         contractor.corporate_staff_name = txt_corporate_staff_name
    #         contractor.email = txt_corporate_staff_email
    #         contractor.tel = txt_corporate_staff_tel
    #         contractor.fax = txt_corporate_staff_fax
    #         contractor.corporate_staff_phone = txt_corporate_staff_phone
    #         # 法人（緊急連絡先）
    #         txt_corporate_contact_tel = request.POST.get('txt_corporate_contact_tel') or None
    #         txt_corporate_contact_name = request.POST.get('txt_corporate_contact_name') or None
    #         txt_corporate_contact_relation = request.POST.get('txt_corporate_contact_relation') or None
    #         contractor.contact_name = txt_corporate_contact_name
    #         contractor.contact_tel = txt_corporate_contact_tel
    #         contractor.contact_relation = txt_corporate_contact_relation
    #     elif rdo_contractor_type == '1':
    #         # 個人連絡先
    #         txt_personal_kana = request.POST.get('txt_personal_kana') or None
    #         txt_personal_name = request.POST.get('txt_personal_name') or None
    #         txt_personal_birthday = request.POST.get('txt_personal_birthday') or None
    #         txt_personal_post1 = request.POST.get('txt_personal_post1') or None
    #         txt_personal_post2 = request.POST.get('txt_personal_post2') or None
    #         txt_personal_address1 = request.POST.get('txt_personal_address1') or None
    #         txt_personal_address2 = request.POST.get('txt_personal_address2') or None
    #         txt_personal_tel = request.POST.get('txt_personal_tel') or None
    #         txt_personal_email = request.POST.get('txt_personal_email') or None
    #         contractor.kana = txt_personal_kana
    #         if txt_personal_name:
    #             contractor.name = txt_personal_name
    #         else:
    #             errors.update({
    #                 'error': True,
    #                 'txt_personal_name': ['氏名は必須項目です。']
    #             })
    #         contractor.personal_birthday = txt_personal_birthday
    #         if txt_personal_post1 and txt_personal_post2:
    #             contractor.post_code = '%s-%s' % (txt_personal_post1, txt_personal_post2)
    #         contractor.address1 = txt_personal_address1
    #         contractor.address2 = txt_personal_address2
    #         contractor.tel = txt_personal_tel
    #         contractor.email = txt_personal_email
    #         # 個人（勤務先）
    #         txt_workplace_name = request.POST.get('txt_workplace_name') or None
    #         txt_workplace_address1 = request.POST.get('txt_workplace_address1') or None
    #         txt_workplace_address2 = request.POST.get('txt_workplace_address2') or None
    #         txt_workplace_tel = request.POST.get('txt_workplace_tel') or None
    #         txt_workplace_fax = request.POST.get('txt_workplace_fax') or None
    #         contractor.workplace_name = txt_workplace_name
    #         contractor.workplace_address1 = txt_workplace_address1
    #         contractor.workplace_address2 = txt_workplace_address2
    #         contractor.workplace_tel = txt_workplace_tel
    #         contractor.workplace_fax = txt_workplace_fax
    #         # 個人（緊急連絡先）
    #         txt_personal_contact_tel = request.POST.get('txt_personal_contact_tel') or None
    #         txt_personal_contact_name = request.POST.get('txt_personal_contact_name') or None
    #         txt_personal_contact_relation = request.POST.get('txt_personal_contact_relation') or None
    #         contractor.contact_name = txt_personal_contact_name
    #         contractor.contact_tel = txt_personal_contact_tel
    #         contractor.contact_relation = txt_personal_contact_relation
    #     else:
    #         errors.update({
    #             'error': True,
    #             'rdo_contractor_type': ['法人か個人か選択してください。']
    #         })
    #     # 媒介
    #     chk_route_flier = request.POST.get('chk_route_flier')
    #     chk_route_internet = request.POST.get('chk_route_internet')
    #     chk_route_board = request.POST.get('chk_route_board')
    #     chk_route_news = request.POST.get('chk_route_news')
    #     chk_route_estate = request.POST.get('chk_route_estate')
    #     chk_route_introduced = request.POST.get('chk_route_introduced')
    #     chk_route_other = request.POST.get('chk_route_other')
    #     txt_route_other = request.POST.get('txt_route_other')
    #     # 順番待ち
    #     rdo_waiting = request.POST.get('rdo_waiting')
    #     if rdo_waiting == 'yes':
    #         pass
    #     elif rdo_waiting == 'no':
    #         pass
    #
    #     if errors.get('error') is False:
    #         try:
    #             if car:
    #                 car.save()
    #                 contract.car = car
    #             contract.save()
    #             contractor.save()
    #             # PDF作成
    #             kwargs.update({'contractor': contractor, 'contract': contract})
    #             title, html = biz.get_subscription_html(request, **kwargs)
    #             data = biz.generate_report_pdf_binary(html)
    #             # 申込書確認のタスクに作成したＰＤＦファイルを追加する。
    #             for report in task.reports.filter(name=constants.REPORT_SUBSCRIPTION):
    #                 report.delete()
    #             content_file = ContentFile(data.getvalue(), name='subscription.pdf')
    #             report_file = models.ReportFile(content_object=task, name=constants.REPORT_SUBSCRIPTION,
    #                                             path=content_file)
    #             report_file.save()
    #             errors.update({'error': False, 'message': '成功しました。'})
    #         except Exception as ex:
    #             logger.error(ex)
    #             errors.update({'error': True, 'message': str(ex)})
    #     return JsonResponse(errors)


class GenerateSubscriptionConfirmPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        subscription = get_object_or_404(Subscription, pk=kwargs.get('subscription_id'))
        title, html = biz.get_subscription_confirm_html(request, subscription, **kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + title
        return response


class GenerateSubscriptionPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        subscription = get_object_or_404(Subscription, pk=kwargs.get('subscription_id'))
        title, html = biz.get_subscription_html(request, subscription, **kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + title
        return response


class UrlTimeoutView(BaseTemplateViewWithoutLogin):
    template_name = 'format/url_timeout.html'


class BaseUserContractView(BaseUserOperationView):

    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            # ステータスが「新規申込み」でない場合は申込み完了に飛ばす
            subscription = get_object_or_404(Subscription, pk=context.get('pk'))
            if subscription.status >= '04' and context.get('is_finished') is False:
                return redirect('format:user_contract_step5', signature=kwargs.get('signature'))
            return self.render_to_response(context)
        except signing.BadSignature:
            return redirect('format:url_timeout')

    def get_context_data(self, **kwargs):
        context = super(BaseUserContractView, self).get_context_data(**kwargs)
        signature = context.get('signature')
        steps = self.get_steps(signature)
        self.request.session['steps'] = steps
        user_subscription = self.get_user_subscription(context.get('pk'))
        context.update({
            'user_subscription': user_subscription,
            'parking_lot': user_subscription.parking_lot,
            'steps': steps,
            'is_all_active': False,
        })
        return context

    def get_steps(self, signature=None):
        return biz.get_user_contract_steps(signature)

    def get_user_subscription(self, subscription_id):
        """ユーザー申込み情報を取得する。

        :return:
        """
        subscription = get_object_or_404(Subscription, pk=subscription_id)
        if 'user_subscription' in self.request.session:
            data = self.request.session['user_subscription']
            if str(data.get('code', 0)) != str(subscription_id):
                data = self.set_user_subscription(subscription)
        else:
            data = self.set_user_subscription(subscription)
        return Subscription(**data)

    def set_user_subscription(self, user_subscription):
        """ユーザー申込み情報をセッションに保存する

        :param user_subscription:
        :return:
        """
        serializer = SubscriptionSerializer(user_subscription)
        self.request.session['user_subscription'] = serializer.data
        return serializer.data


class UserContractStep1View(BaseUserContractView):
    template_name = 'format/user_contract_step1.html'

    def get_context_data(self, **kwargs):
        context = super(UserContractStep1View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[0]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        return redirect('format:user_contract_step2', signature=kwargs.get('signature'))


class UserContractStep2View(BaseUserContractView):
    template_name = 'format/user_contract_step2.html'

    def get_context_data(self, **kwargs):
        context = super(UserContractStep2View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[1]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        return redirect('format:user_contract_step3', signature=kwargs.get('signature'))


class UserContractStep3View(BaseUserContractView):
    template_name = 'format/user_contract_step3.html'

    def get_context_data(self, **kwargs):
        context = super(UserContractStep3View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[2]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        return redirect('format:user_contract_step4', signature=kwargs.get('signature'))


class UserContractStep4View(BaseUserContractView):
    template_name = 'format/user_contract_step4.html'

    def get_context_data(self, **kwargs):
        context = super(UserContractStep4View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[3]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        context = super(UserContractStep4View, self).get_context_data(**kwargs)
        user_subscription = context.get('user_subscription')
        # 契約完了、ユーザーサイン済み
        # user_subscription.status = '04'
        # user_subscription.save()
        # self.set_user_subscription(user_subscription)
        # 通知（メールとプッシュ）
        parking_lot = context.get('parking_lot')
        # mail_group = MailGroup.get_contract_form_completed_group()
        # data = user_subscription.get_subscription_addressee()
        # mail_group.send_main(user_subscription.get_subscription_email(), data)
        push_notification(
            '%s 契約完了' % str(parking_lot),
            '',
            url=reverse('contract:subscription_detail', args=(user_subscription.pk,)),
        )
        return redirect('format:user_contract_step5', signature=kwargs.get('signature'))


class UserContractStep5View(BaseUserContractView):
    template_name = 'format/user_contract_step5.html'

    def get_context_data(self, **kwargs):
        context = super(UserContractStep5View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[4]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
            'is_finished': True
        })
        return context


class BaseContractCancellationView(BaseUserOperationView):

    def get(self, request, *args, **kwargs):
        try:
            context = self.get_context_data(**kwargs)
            # ステータスが「新規申込み」でない場合は申込み完了に飛ばす
            # cancellation = get_object_or_404(ContractCancellation, pk=context.get('pk'))
            # if subscription.status >= '04' and context.get('is_finished') is False:
            #     return redirect('format:user_contract_step4', signature=kwargs.get('signature'))
            return self.render_to_response(context)
        except signing.BadSignature:
            return redirect('format:url_timeout')

    def get_context_data(self, **kwargs):
        context = super(BaseContractCancellationView, self).get_context_data(**kwargs)
        signature = context.get('signature')
        steps = self.get_steps(signature)
        self.request.session['steps'] = steps
        cancellation = self.get_cancellation(context.get('pk'))
        context.update({
            'cancellation': cancellation,
            'parking_lot': cancellation.parking_lot,
            'contractor': cancellation.contractor,
            'contract': cancellation.contract,
            'steps': steps,
            'is_all_active': False,
        })
        return context

    def get_steps(self, signature=None):
        return biz.get_contract_cancellation_steps(signature)

    def get_cancellation(self, cancellation_id):
        """ユーザー申込み情報を取得する。

        :return:
        """
        cancellation = get_object_or_404(ContractCancellation, pk=cancellation_id)
        if 'contract_cancellation' in self.request.session:
            data = self.request.session['contract_cancellation']
            if str(data.get('pk', 0)) != str(cancellation_id):
                data = self.set_cancellation(cancellation)
        else:
            data = self.set_cancellation(cancellation)
        data['contract'] = get_object_or_404(Contract, pk=data['contract'])
        data['parking_lot'] = get_object_or_404(ParkingLot, pk=data['parking_lot'])
        data['parking_position'] = get_object_or_404(ParkingPosition, pk=data['parking_position'])
        data['contractor'] = get_object_or_404(Contractor, pk=data['contractor'])
        data['reception_user'] = get_object_or_404(User, pk=data['reception_user'])
        return ContractCancellation(**data)

    def set_cancellation(self, cancellation):
        """ユーザー申込み情報をセッションに保存する

        :param cancellation:
        :return:
        """
        serializer = ContractCancellationSerializer(cancellation)
        self.request.session['contract_cancellation'] = serializer.data
        return serializer.data


class ContractCancellationStep1View(BaseContractCancellationView):
    template_name = 'format/contract_cancellation_step1.html'

    def get_context_data(self, **kwargs):
        context = super(ContractCancellationStep1View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[0]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
        })
        return context

    def post(self, request, *args, **kwargs):
        return redirect('format:user_contract_cancellation_step2', signature=kwargs.get('signature'))


class ContractCancellationStep2View(BaseContractCancellationView):
    template_name = 'format/contract_cancellation_step2.html'

    def get_context_data(self, **kwargs):
        context = super(ContractCancellationStep2View, self).get_context_data(**kwargs)
        steps = context.get('steps')
        current_step = steps[1]
        context.update({
            'title': current_step.get('name'),
            'current_step': current_step,
            'is_finished': True,
        })
        return context
