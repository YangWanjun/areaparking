import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.validators import RegexValidator, validate_comma_separated_integer_list
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.functional import cached_property

from employee.models import Member
from format.models import ReportFile, ReportSubscription, ReportSubscriptionConfirm
from master.models import Mediation, BankAccount, Config, Payment, MailGroup, TransmissionRoute
from parkinglot.models import ParkingLot, ParkingPosition, ParkingLotType, LeaseManagementCompany, \
    BuildingManagementCompany
from utils import constants, common, errors
from utils.app_base import get_total_context, \
    get_user_subscription_simple_url, \
    get_user_subscription_inspection_url, \
    get_user_contract_url, \
    get_parking_lot_context, \
    get_subscription_context, \
    get_contractor_context, \
    get_contract_cancellation_url
from utils.django_base import BaseModel, PublicManager, BaseViewModel


# Create your models here.
class AbstractUser(BaseModel):
    code = models.AutoField(primary_key=True, verbose_name="契約者No.")
    category = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_CONTRACTOR_TYPE,
                                verbose_name="契約者分類")
    name = models.CharField(max_length=30, verbose_name="名前")
    kana = models.CharField(blank=True, null=True, max_length=30, verbose_name="カナ")
    post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name="郵便番号",
                                 validators=(RegexValidator(regex=constants.REG_POST_CODE),))
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    comment = models.CharField(blank=True, null=True, max_length=255, verbose_name="備考")
    # 個人情報
    personal_phone = models.CharField(blank=True, null=True, max_length=15, verbose_name="携帯電話")
    personal_gender = models.CharField(max_length=1, blank=True, null=True, choices=constants.CHOICE_GENDER,
                                       verbose_name="性別")
    personal_birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")
    # 法人情報
    corporate_business_type = models.CharField(blank=True, null=True, max_length=50, verbose_name="業種／事業")
    corporate_web_site = models.URLField(blank=True, null=True, verbose_name="ホームページ")
    corporate_president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
    corporate_staff_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"担当者名")
    corporate_staff_kana = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"担当者カナ")
    corporate_staff_email = models.EmailField(blank=True, null=True, verbose_name="担当者Email")
    corporate_staff_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"担当者電話番号")
    corporate_staff_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"担当者ファックス")
    corporate_staff_phone = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"担当者携帯電話")
    corporate_staff_department = models.CharField(blank=True, null=True, max_length=30, verbose_name="担当者所属")
    corporate_staff_position = models.CharField(blank=True, null=True, max_length=30, verbose_name="担当者役職")
    corporate_capital = models.IntegerField(blank=True, null=True, verbose_name="資本金")
    corporate_turnover = models.IntegerField(blank=True, null=True, verbose_name="年収／年商")
    corporate_user_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"使用者名")
    corporate_user_kana = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"使用者カナ")
    corporate_user_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"使用者携帯電話")
    corporate_user_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name="使用者所在地郵便番号",
                                                validators=(RegexValidator(regex=constants.REG_POST_CODE),))
    corporate_user_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"使用者所在地１")
    # 勤務先
    workplace_name = models.CharField(blank=True, null=True, max_length=100, verbose_name="勤務先名称")
    workplace_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"勤務先郵便番号")
    workplace_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"勤務先住所１")
    workplace_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"勤務先住所２")
    workplace_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"勤務先電話番号")
    workplace_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"勤務先ファックス")
    workplace_comment = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"備考",
                                         help_text='勤務先のない方は、ご家族の勤務先と、その方のお名前・関係性をお知らせください。')
    # 連絡先
    contact_name = models.CharField(blank=True, null=True, max_length=15, verbose_name="連絡先名称")
    contact_kana = models.CharField(blank=True, null=True, max_length=15, verbose_name="連絡先カナ")
    contact_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"連絡先郵便番号")
    contact_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"連絡先住所１")
    contact_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"連絡先住所２")
    contact_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"連絡先電話番号")
    contact_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"連絡先ファックス")
    contact_relation = models.CharField(blank=True, null=True, max_length=20, verbose_name="連絡先との間柄")
    # 書類送付先
    delivery_type = models.CharField(blank=True, null=True, max_length=2,
                                     choices=constants.CHOICE_PAPER_DELIVERY_TYPE, verbose_name="書類送付先区分")
    delivery_honorific = models.CharField(max_length=1, blank=True, null=True,
                                          choices=constants.CHOICE_HONORIFIC, verbose_name="宛名敬称")
    delivery_name = models.CharField(blank=True, null=True, max_length=30, verbose_name="送付先名称")
    delivery_kana = models.CharField(blank=True, null=True, max_length=30, verbose_name="送付先カナ")
    delivery_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"送付先郵便番号")
    delivery_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"送付先住所１")
    delivery_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"送付先住所２")
    delivery_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"送付先電話番号")
    delivery_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"送付先ファックス")
    # 保証人
    guarantor_name = models.CharField(blank=True, null=True, max_length=15, verbose_name="保証人名称")
    guarantor_kana = models.CharField(blank=True, null=True, max_length=15, verbose_name="保証人カナ")
    guarantor_birthday = models.DateField(blank=True, null=True, verbose_name="保証人生年月日")
    guarantor_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"保証人郵便番号")
    guarantor_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"保証人住所１")
    guarantor_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"保証人住所２")
    guarantor_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"保証人電話番号")
    guarantor_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"保証人ファックス")
    guarantor_relation = models.CharField(blank=True, null=True, max_length=20, verbose_name="保証人との間柄")
    guarantor_comment = models.CharField(blank=True, null=True, max_length=255, verbose_name="備考")
    # 仮契約であるかどうかのステータス
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_CONTRACT_STATUS, editable=False,
                              verbose_name="ステータス")
    payee_bank_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.SET_NULL,
                                           verbose_name="口座")

    objects = PublicManager(is_deleted=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def address(self):
        return '%s%s' % ((self.address1 or ''), (self.address2 or ''))


class AbstractCar(BaseModel):
    car_maker = models.CharField(max_length=50, blank=True, null=True, verbose_name="車メーカー")
    car_model = models.CharField(max_length=100, blank=True, null=True, verbose_name="車種")
    car_color = models.CharField(max_length=10, blank=True, null=True, verbose_name="色")
    car_no_plate = models.CharField(max_length=20, blank=True, null=True, verbose_name="No.プレート")
    car_length = models.IntegerField(blank=True, null=True, verbose_name="全長")
    car_width = models.IntegerField(blank=True, null=True, verbose_name="全幅")
    car_height = models.IntegerField(blank=True, null=True, verbose_name="全高")
    car_weight = models.IntegerField(blank=True, null=True, verbose_name="重量")
    car_min_height = models.IntegerField(blank=True, null=True, verbose_name="地上最低高")
    car_f_value = models.IntegerField(blank=True, null=True, verbose_name="F値")
    car_r_value = models.IntegerField(blank=True, null=True, verbose_name="R値")
    car_comment = models.CharField(max_length=200, blank=True, null=True, verbose_name="車の備考")
    insurance_limit_type = models.CharField(blank=True, null=True, max_length=10,
                                            choices=constants.CHOICE_INSURANCE_TYPE, verbose_name="保険制限")
    insurance_limit_amount = models.IntegerField(blank=True, null=True, verbose_name="対物限度額")
    insurance_expire_date = models.DateField(blank=True, null=True, verbose_name='保険の有効期限')

    class Meta:
        abstract = True

    def __str__(self):
        return self.car_model or ''


class Contractor(AbstractUser):
    temp_objects = PublicManager(is_deleted=False, status='01')
    real_objects = PublicManager(is_deleted=False, status='11')

    class Meta:
        db_table = 'ap_contractor'
        ordering = ['name']
        verbose_name = "契約者"
        verbose_name_plural = "契約者一覧"

    def get_current_contracts(self):
        """現在の契約を取得する。

        :return:
        """
        today = datetime.date.today()
        queryset = Contract.objects.public_filter(contractor=self, start_date__lte=today, end_date__gte=today)
        return queryset


def get_default_subscription_format_id():
    report = ReportSubscription.get_default_report()
    return report.pk if report else None


def get_default_subscription_confirm_format_id():
    report = ReportSubscriptionConfirm.get_default_report()
    return report.pk if report else None


class Subscription(AbstractUser, AbstractCar):
    parking_lot_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="申込みする駐車場")
    parking_position_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="申込みする車室")
    post_code1 = models.CharField(blank=True, null=True, max_length=3, verbose_name="郵便番号１")
    post_code2 = models.CharField(blank=True, null=True, max_length=4, verbose_name="郵便番号２")
    workplace_post_code1 = models.CharField(blank=True, null=True, max_length=3, verbose_name=u"勤務先郵便番号１")
    workplace_post_code2 = models.CharField(blank=True, null=True, max_length=4, verbose_name=u"勤務先郵便番号２")
    corporate_user_post_code1 = models.CharField(blank=True, null=True, max_length=3, verbose_name=u"使用者所在地郵便番号１")
    corporate_user_post_code2 = models.CharField(blank=True, null=True, max_length=4, verbose_name=u"使用者所在地郵便番号２")
    contract_start_date = models.DateField(blank=True, null=True, verbose_name='希望契約開始日')
    contract_period = models.CharField(blank=True, null=True, max_length=5, choices=constants.CHOICE_CONTRACT_PERIOD,
                                       verbose_name="希望契約期間")
    contract_end_month = models.IntegerField(blank=True, null=True, verbose_name="短期契約の終了月")
    require_receipt = models.CharField(blank=True, null=True, max_length=3, choices=constants.CHOICE_IS_REQUIRED,
                                       verbose_name="保管証発行-車庫証明")
    require_waiting = models.CharField(blank=True, null=True, max_length=3, choices=constants.CHOICE_IS_REQUIRED,
                                       verbose_name="順番待ち", help_text='申込書の到着時点で当駐車場が満車になっていた場合､順番待ちを希望しますか？')
    transmission_routes = models.CharField(blank=True, null=True, max_length=20, verbose_name="媒体",
                                           validators=[validate_comma_separated_integer_list],
                                           help_text='どのようにして､この駐車場を知りましたか？')
    transmission_other_route = models.CharField(blank=True, null=True, max_length=50, verbose_name="その他の媒体")
    # 申込みのステータス
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_SUBSCRIPTION_STATUS, editable=False,
                              verbose_name="ステータス")
    subscription_confirm_format_id = models.PositiveIntegerField(blank=True, null=True,
                                                                 default=get_default_subscription_confirm_format_id,
                                                                 verbose_name="申込確認書のフォーマット")
    subscription_format_id = models.PositiveIntegerField(blank=True, null=True,
                                                         default=get_default_subscription_format_id,
                                                         verbose_name="申込書のフォーマット")
    reports = GenericRelation(ReportFile, related_query_name='subscriptions')
    contacts = GenericRelation('ContactHistory', related_query_name='subscription_set')
    created_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u"作成日時")
    updated_date = models.DateTimeField(auto_now=True, editable=False, verbose_name=u"更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)
    temp_objects = PublicManager(is_deleted=False, status__lt='11')

    class Meta:
        db_table = 'ap_subscription'
        ordering = ['name']
        verbose_name = "契約手続き"
        verbose_name_plural = "契約手続き一覧"

    @cached_property
    def parking_lot(self):
        if self.parking_lot_id:
            try:
                return ParkingLot.objects.get(pk=self.parking_lot_id)
            except ObjectDoesNotExist:
                return None
        else:
            return None

    @cached_property
    def parking_position(self):
        if self.parking_position_id:
            try:
                return ParkingPosition.objects.get(pk=self.parking_position_id)
            except ObjectDoesNotExist:
                return None
        else:
            return None

    @cached_property
    def subscription_confirm_format(self):
        if self.subscription_confirm_format_id:
            try:
                return ReportSubscriptionConfirm.objects.get(pk=self.subscription_confirm_format_id)
            except ObjectDoesNotExist:
                return None
        else:
            return None

    @cached_property
    def subscription_format(self):
        if self.subscription_format_id:
            try:
                return ReportSubscription.objects.get(pk=self.subscription_format_id)
            except ObjectDoesNotExist:
                return None
        else:
            return None

    @cached_property
    def process(self):
        """申込みから成約までのプロセスを取得する

        :return:
        """
        try:
            subscription_type = ContentType.objects.get_for_model(self)
            return Process.objects.get(content_type__pk=subscription_type.pk, object_id=self.pk)
        except ObjectDoesNotExist:
            return None

    @cached_property
    def tasks(self):
        """タスクリストを取得する

        :return:
        """
        return self.process.task_set.all()

    @cached_property
    def percent(self):
        """完成度を取得する

        :return:
        """
        process = self.process
        if process:
            return process.percent
        else:
            return 0.0

    @property
    def is_require_receipt(self):
        """保管証発行-車庫証明は必要なのか

        :return:
        """
        return self.require_receipt == 'yes'

    def get_post_code(self):
        if self.post_code1 and self.post_code2:
            return '%s-%s' % (self.post_code1, self.post_code2)
        else:
            return None

    def get_corporate_user_post_code(self):
        if self.corporate_user_post_code1 and self.corporate_user_post_code2:
            return '%s-%s' % (self.corporate_user_post_code1, self.corporate_user_post_code2)
        else:
            return None

    def get_workplace_post_code(self):
        if self.workplace_post_code1 and self.workplace_post_code2:
            return '%s-%s' % (self.workplace_post_code1, self.workplace_post_code2)
        else:
            return None

    def get_suitable_positions(self):
        """駐車可能の車室を取得する

        :return:
        """
        positions = self.parking_lot.get_suitable_positions(self.car_length, self.car_width,
                                                            self.car_height, self.car_weight)
        return positions

    def get_contract_start_date(self):
        """契約開始日を取得する。

        :return:
        """
        start_date = self.contract_start_date
        if not start_date:
            start_date = datetime.date.today()
        if start_date and isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        return start_date

    def get_contract_end_date(self):
        """長期契約の場合の契約更新日を自動設置

        :return:
        """
        # 駐車場の既定の契約期間を設置
        default_period = self.parking_lot.default_contract_months
        start_date = self.get_contract_start_date()
        if start_date.day == 1:
            default_period -= 1

        date = common.add_months(start_date, default_period)
        return common.get_last_day_by_month(date)

    def get_notify_start_date(self):
        """契約終了通知開始日を取得する

        デフォルトは１か月前

        :return:
        """
        start_date = None
        contract_end_date = self.get_contract_end_date()
        if contract_end_date:
            start_date = common.add_months(contract_end_date, -1)
            start_date = common.get_first_day_by_month(start_date)
        return start_date

    def get_notify_end_date(self):
        """契約終了通知終了日を取得する

        デフォルトは１か月前

        :return:
        """
        end_date = None
        contract_end_date = self.get_contract_end_date()
        if contract_end_date:
            end_date = common.add_months(contract_end_date, -1)
            end_date = common.get_last_day_by_month(end_date)
        return end_date

    def get_subscription_email(self):
        """申込み完了時のメール宛先アドレス

        :return:
        """
        if self.category == '1':
            # 個人
            return self.email
        else:
            return self.corporate_staff_email

    def get_subscription_addressee(self):
        """申込み完了時、メール送信の宛名と敬称

        :return:
        """
        return {
            'user_name': self.name,
            'user_honorific': '様' if self.category == '1' else '御中'
        }

    def get_monthly_rent(self):
        """月分の賃料（税抜）を取得する。

        デフォルトはホームページ価格

        :return:
        """
        price = 0
        if self.parking_position:
            price = self.parking_position.price_homepage_no_tax or 0
            if self.transmission_routes:
                for route_id in self.transmission_routes.split(','):
                    try:
                        transmission_route = TransmissionRoute.objects.get(pk=route_id)
                        if transmission_route.price_kbn == '01':
                            price = self.parking_position.price_handbill_no_tax or 0
                    except ObjectDoesNotExist:
                        pass
        return price

    def get_current_month_rent(self):
        """契約開始月末日までの賃料

        :return:
        """
        monthly_price = self.get_monthly_rent()
        if monthly_price and self.contract_start_date and self.contract_start_date.day != 1:
            days = common.get_days_by_month(self.contract_start_date) - self.contract_start_date.day - 1
            return common.get_integer(monthly_price / days, Config.get_decimal_type()) * days
        else:
            return 0

    def get_current_month_payments(self):
        """契約開始月の支払項目

        :return:
        """
        queryset = ContractPayment.objects.public_filter(subscription=self, timing='11')
        return queryset

    def get_current_month_payments_total(self):
        return self.get_current_month_payments().aggregate(Sum('amount'), Sum('consumption_tax'))

    def get_monthly_payments(self):
        """翌月以降の支払項目

        :return:
        """
        queryset = ContractPayment.objects.public_filter(subscription=self, timing='30')
        return queryset

    def get_monthly_payments_total(self):
        summary = self.get_monthly_payments().aggregate(Sum('amount'), Sum('consumption_tax'))
        summary['total'] = (summary.get('amount__sum', 0) or 0) + (summary.get('consumption_tax__sum', 0) or 0)
        return summary

    def get_contracting_payments(self):
        """契約時の支払項目

        :return:
        """
        queryset = ContractPayment.objects.public_filter(subscription=self, timing__startswith='4')
        return queryset

    def get_contracting_payments_total(self):
        return self.get_contracting_payments().aggregate(Sum('amount'), Sum('consumption_tax'))

    def get_contract_payments_total(self):
        queryset = ContractPayment.objects.public_filter(subscription=self, timing__in=['11', '30', '40', '41'])
        summary = queryset.aggregate(Sum('amount'), Sum('consumption_tax'))
        summary['total'] = (summary.get('amount__sum', 0) or 0) + (summary.get('consumption_tax__sum', 0) or 0)
        return summary

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_new = True if self.pk is None else False
        if is_new:
            # 貸止、空き無の場合は作成できない。
            if self.parking_position.is_lock:
                raise errors.CustomException(constants.ERROR_SUBSCRIPTION_LOCKED)
            if self.parking_position.get_current_contract():
                raise errors.CustomException(constants.ERROR_SUBSCRIPTION_CONTRACTED)
        super(Subscription, self).save(force_insert, force_update, using, update_fields)
        if is_new:
            # 進捗のプロセス作成
            process = Process.objects.create(name='01', content_object=self)
            for i, category in enumerate(constants.CHOICE_TASK_SUBSCRIPTION_CATEGORY, 1):
                task = Task(process=process, order=i, category=category[0], name=category[1])
                if i == len(constants.CHOICE_TASK_SUBSCRIPTION_CATEGORY):
                    task.is_end = True
                task.save()
            # 入金項目作成
            payments = Payment.objects.public_filter(is_active=True, is_initial=True)
            consumption_tax_rate = Config.get_consumption_tax_rate()
            decimal_type = Config.get_decimal_type()
            for payment in payments:
                contract_payment = ContractPayment(subscription=self, timing=payment.timing, payment=payment)
                contract_payment.amount = payment.amount or 0
                if payment.timing == '11':
                    # 契約開始月
                    contract_payment.amount = self.get_current_month_rent()
                elif payment.timing == '30':
                    # 翌月以降
                    contract_payment.amount = self.get_monthly_rent()
                contract_payment.consumption_tax = common.get_integer(contract_payment.amount * consumption_tax_rate,
                                                                      decimal_type)
                contract_payment.save()
        # 保管証発行-車庫証明
        if self.is_require_receipt:
            payment = Payment.objects.get(timing='41')
            if ContractPayment.objects.public_filter(timing='41').count() == 0:
                contract_payment = ContractPayment(subscription=self, timing='41', payment=payment)
                # TODO: 保管証発行-車庫証明の入金項目作成

    def delete(self, using=None, keep_parents=False):
        # プロセスを削除する
        if self.process:
            Task.objects.public_filter(process=self.process).delete()
            self.process.delete()
        # 入金項目を削除
        ContractPayment.objects.public_filter(subscription=self).delete()
        # 申込み情報を削除
        super(Subscription, self).delete(using, keep_parents)

    parking_lot.short_description = '駐車場'
    parking_position.short_description = '車室'
    percent.short_description = '進捗'


class ContractorCar(AbstractCar):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name="契約者")

    class Meta:
        db_table = 'ap_contractor_car'
        ordering = ['contractor', 'car_maker', 'car_model']
        verbose_name = "保有車"
        verbose_name_plural = "保有車一覧"


class Contract(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, blank=True, null=True, on_delete=models.PROTECT, verbose_name="契約者")
    subscription = models.ForeignKey(Subscription, blank=True, null=True, on_delete=models.PROTECT, verbose_name="申込者")
    # 基本情報
    contract_date = models.DateField(blank=True, null=True, verbose_name="契約日")
    start_date = models.DateField(blank=True, null=True, verbose_name="契約開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name="契約終了日")
    notify_start_date = models.DateField(blank=True, null=True, verbose_name="契約終了通知開始日")
    notify_end_date = models.DateField(blank=True, null=True, verbose_name="契約終了通知終了日")
    staff = models.ForeignKey(Member, verbose_name="担当者")
    transmission_route = models.ForeignKey(TransmissionRoute, blank=True, null=True, verbose_name="媒体")
    mediation = models.ForeignKey(Mediation, blank=True, null=True, verbose_name="仲介業者")
    staff_assistant1 = models.ForeignKey(Member, null=True, blank=True, related_name='contract_assistant1_set',
                                         verbose_name="アシスタント１")
    staff_assistant2 = models.ForeignKey(Member, null=True, blank=True, related_name='contract_assistant2_set',
                                         verbose_name="アシスタント２")
    staff_assistant3 = models.ForeignKey(Member, null=True, blank=True, related_name='contract_assistant3_set',
                                         verbose_name="アシスタント３")
    # 口座情報
    payee_bank_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.PROTECT,
                                           verbose_name="振込先口座")
    # 車情報
    car = models.ForeignKey(ContractorCar, blank=True, null=True, verbose_name="契約する車")
    # 仮契約であるかどうかのステータス
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_CONTRACT_STATUS, editable=False,
                              verbose_name="ステータス")
    processes = GenericRelation('Process', related_query_name='contracts')

    objects = PublicManager(is_deleted=False)
    temp_objects = PublicManager(is_deleted=False, status='01')
    real_objects = PublicManager(is_deleted=False, status='11')

    class Meta:
        db_table = 'ap_contract'
        ordering = ['contractor', 'start_date']
        verbose_name = "契約情報"
        verbose_name_plural = "契約情報一覧"

    def __str__(self):
        if self.contractor:
            name = str(self.contractor)
        else:
            name = str(self.subscription)
        return '%s（%s～%s）' % (name, self.start_date, self.end_date)

    def get_contract_end_date(self):
        """長期契約の場合の契約更新日を自動設置

        :return:
        """
        # 駐車場の既定の契約期間を設置
        default_period = self.parking_lot.default_contract_months
        if self.start_date.day == 1:
            default_period -= 1

        date = common.add_months(self.start_date, default_period)
        return common.get_last_day_by_month(date)

    def get_monthly_price(self):
        """月分の賃料（税抜）を取得する。

        デフォルトはホームページ価格

        :return:
        """
        price = 0
        if self.parking_position:
            price = self.parking_position.price_homepage_no_tax or 0
            if self.transmission_route and self.transmission_route.price_kbn == '01':
                price = self.parking_position.price_handbill_no_tax or 0
        return price

    def get_current_month_price(self):
        """契約開始月末日までの賃料

        :return:
        """
        monthly_price = self.get_monthly_price()
        if monthly_price and self.start_date and self.start_date.day != 1:
            days = common.get_days_by_month(self.start_date) - self.start_date.day - 1
            return common.get_integer(monthly_price / days, Config.get_decimal_type()) * days
        else:
            return 0

    def get_process_list(self):
        """契約に関する随時対応のプロセスを取得する。

        :return:
        """
        process_list = []
        for code, name in constants.CHOICE_PROCESS:
            if code >= '10':
                process_list.append((code, name, self.processes.filter(name=code)))
        return process_list

    @cached_property
    def parking_position_cancellation_without_continue_process(self):
        """物件解約（継承なし）のおプロセスを取得する。

        :return:
        """
        if hasattr(self, 'parkingpositioncancellation'):
            return self.parkingpositioncancellation.processes.filter(name='32').first()
        else:
            return None

    @cached_property
    def parking_position_cancellation_with_continue_process(self):
        """物件解約（継承あり）のプロセスを取得する。

        :return:
        """
        if hasattr(self, 'parkingpositioncancellation'):
            return self.parkingpositioncancellation.processes.filter(name='33').first()
        else:
            return None


class ContractPayment(BaseModel):
    subscription = models.ForeignKey(Subscription, verbose_name="申込情報")
    contract = models.ForeignKey(Contract, blank=True, null=True, verbose_name="契約情報")
    timing = models.CharField(max_length=2, choices=constants.CHOICE_PAY_TIMING, verbose_name="タイミング")
    payment = models.ForeignKey(Payment, verbose_name="入金項目")
    amount = models.IntegerField(verbose_name="請求額")
    consumption_tax = models.IntegerField(verbose_name="消費税")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_contract_payment'
        ordering = ['timing']
        verbose_name = "入金項目"
        verbose_name_plural = "入金項目一覧"

    def __str__(self):
        return str(self.payment)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.consumption_tax = self.payment.get_consumption_tax(self.amount)
        super(ContractPayment, self).save(force_insert, force_update, using, update_fields)


class Process(BaseModel):
    name = models.CharField(max_length=2, choices=constants.CHOICE_PROCESS, verbose_name="プロセス名称")
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'ap_process'
        verbose_name = "プロセス"
        verbose_name_plural = "プロセス一覧"

    @cached_property
    def percent(self):
        """進捗の完成度（%）を取得

        :return:
        """
        task_count = Task.objects.public_filter(process=self).count()
        if task_count == 0:
            return 0.0
        else:
            # スキップと完了したタスク数
            finished_count = Task.objects.public_filter(process=self, status__in=['10', '99']).count()
            return round((finished_count / task_count) * 100, 1)

    @cached_property
    def contractor(self):
        return self.content_object.contractor

    @cached_property
    def parking_lot(self):
        return self.content_object.parking_lot

    @cached_property
    def parking_position(self):
        return self.content_object.parking_position

    @cached_property
    def is_finished(self):
        """プロセスは完了したかどうかを判断する。

        :return:
        """
        # 完了またはスキップしたタスク数
        finished_count = Task.objects.public_filter(process=self, status=['10', '99']).count()
        # 総タスク数
        all_count = Task.objects.public_filter(process=self).count()
        return finished_count == all_count

    percent.short_description = '進捗'
    contractor.short_description = '契約者'
    parking_lot.short_description = '駐車場'
    parking_position.short_description = '車室'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_new = True if self.pk is None else False
        super(Process, self).save(force_insert, force_update, using, update_fields)
        if is_new and self.name != '01':
            for i, category in enumerate(constants.CHOICE_TASK_CATEGORY, 1):
                code, name = category
                if code.startswith(self.name):
                    task = Task(process=self, order=i, category=code, name=name)
                    task.save()


class Task(BaseModel):
    process = models.ForeignKey(Process, verbose_name="契約進捗")
    category = models.CharField(max_length=3, choices=constants.CHOICE_TASK_CATEGORY, verbose_name="タスク名称")
    name = models.CharField(max_length=50, verbose_name="タスク名称")
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_TASK_STATUS, verbose_name='ステータス')
    updated_user = models.ForeignKey(User, blank=True, null=True, verbose_name="更新ユーザー")
    url_links = models.CharField(max_length=2000, blank=True, null=True, verbose_name="リンク")
    order = models.SmallIntegerField(verbose_name="並び順")
    is_end = models.BooleanField(default=False, verbose_name="終了タスク")

    class Meta:
        db_table = 'ap_task'
        unique_together = ['process', 'category']
        ordering = ['process', 'order']
        verbose_name = "タスク"
        verbose_name_plural = "タスク一覧"

    def __str__(self):
        return self.name

    def get_mail_group(self):
        group = None
        if self.category == '010':
            # 申込書送付
            group = MailGroup.get_subscription_send_group()
        elif self.category == '012':
            # 審査用フォーム送付
            group = MailGroup.get_inspection_send_group()
        elif self.category == '040':
            # 契約書類一式の送付
            group = MailGroup.get_contract_form_send_group()
        elif self.category == "042":
            # 契約書の送付
            group = MailGroup.get_contract_send_group()
        elif self.category == "060":
            # 鍵類、操作説明書、配置図送付
            group = MailGroup.get_contract_other_send_group()
        elif self.category == '310':
            # 一般解約の送付
            group = MailGroup.get_contract_cancellation_send_group()
        elif self.category == '322':
            group = MailGroup.get_parking_lot_cancellation_send_group()
        return group

    def get_mail_template(self):
        group = self.get_mail_group()
        if group:
            data = get_total_context()
            if self.category == '010':
                data.update(get_parking_lot_context(self.process.content_object.parking_lot))
                data.update(get_subscription_context(self.process.content_object))
                data.update(get_user_subscription_simple_url(self))
            elif self.category == '012':
                data.update(get_parking_lot_context(self.process.content_object.parking_lot))
                data.update(get_subscription_context(self.process.content_object))
                data.update(get_user_subscription_inspection_url(self))
            elif self.category == '040':
                data.update(get_parking_lot_context(self.process.content_object.parking_lot))
                data.update(get_subscription_context(self.process.content_object))
                data.update(get_user_contract_url(self))
            elif self.category == '042':
                data.update(get_parking_lot_context(self.process.content_object.parking_lot))
                data.update(get_subscription_context(self.process.content_object))
            elif self.category == '060':
                data.update(get_parking_lot_context(self.process.content_object.parking_lot))
                data.update(get_subscription_context(self.process.content_object))
            elif self.category == '310':
                # 一般解約の送付
                data.update(get_parking_lot_context(self.process.content_object.parking_lot))
                data.update(get_contractor_context(self.process.content_object.contractor))
                data.update(get_contract_cancellation_url(self))
            elif self.category == '322':
                # 物件解約（継承なし）時の書類送付
                data.update(get_parking_lot_context(self.process.content_object.parking_lot))
                data.update(get_contractor_context(self.process.content_object.contractor))

            return group.get_template_content(data)
        else:
            return dict()

    def get_prev_task(self):
        """前のタスクを取得する。

        :return:
        """
        if self.category == '011':
            # 申込書確認の場合、申込書送付のタスクを取得する。
            try:
                return Task.objects.get(process=self.process, category='010')
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def get_next_task(self):
        """次のタスクを取得する。

        :return:
        """
        if self.category == '010':
            # 申込書送付の場合、申込書確認のタスクを取得する。
            try:
                return Task.objects.get(process=self.process, category='011')
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def is_finished(self):
        """タスクが成功完了

        :return:
        """
        return self.status == '99'

    def is_skipped(self):
        """タスクはスキップした

        :return:
        """
        return self.status == '10'

    def is_failure(self):
        """タスクが通らない

        :return:
        """
        return self.status == '20'

    def can_continue(self):
        if self.is_finished() or self.is_skipped():
            return True
        else:
            return False


class ContractCancellation(BaseModel):
    contract = models.OneToOneField(Contract, on_delete=models.PROTECT, verbose_name="契約情報")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
    cancellation_date = models.DateField(verbose_name="解約日")
    retire_date = models.DateField(blank=True, null=True, verbose_name="退居予定日")
    reception_user = models.ForeignKey(User, verbose_name="受付者")
    processes = GenericRelation('Process', related_query_name='contract_cancellations')

    class Meta:
        db_table = 'ap_contract_cancellation'
        verbose_name = "一般解約"
        verbose_name_plural = "一般解約一覧"

    def __str__(self):
        return '%s - %s：%s' % (self.parking_lot, self.parking_position, self.cancellation_date)

    @cached_property
    def process(self):
        """解約のプロセスを取得する。

        :return:
        """
        try:
            return self.processes.get(name='31')
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # if self.retire_date:
        #     if self.retire_date > self.cancellation_date:
        #         raise errors.CustomException(constants.ERROR_CONTRACT_WRONG_RETIRE_DATE)
        #     elif self.retire_date > self.contract.end_date or self.retire_date < self.contract.start_date:
        #         raise errors.CustomException(constants.ERROR_CONTRACT_RETIRE_DATE_RANGE)
        if self.cancellation_date > self.contract.end_date or self.cancellation_date < self.contract.start_date:
            raise errors.CustomException(constants.ERROR_CONTRACT_CANCELLATION_DATE_RANGE)
        super(ContractCancellation, self).save(force_insert, force_update, using, update_fields)
        # 解約のプロセスを作成
        Process.objects.create(name='31', content_object=self)


class ParkingLotCancellation(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_positions = models.CharField(max_length=100, blank=True, null=True,
                                         validators=[validate_comma_separated_integer_list], verbose_name="返却車室")
    is_all = models.BooleanField(default=False, verbose_name="全件解約")
    is_immediately = models.BooleanField(default=False, verbose_name="随時返還")
    is_with_continue = models.BooleanField(default=False, verbose_name="継承あり")
    contact_date = models.DateField(verbose_name="告知日")
    created_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="作成者")
    return_date = models.DateField(blank=True, null=True, verbose_name="返却リミット")

    class Meta:
        db_table = 'ap_parking_lot_cancellation'
        verbose_name = "物件解約"
        verbose_name_plural = "物件解約一覧"

    def __str__(self):
        return str(self.parking_lot)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk:
            is_add = False
        else:
            is_add = True
        if not self.is_all and not self.parking_positions:
            raise errors.CustomException(constants.ERROR_PARKING_LOT_CANCELLATION_NO_POSITIONS)
        super(ParkingLotCancellation, self).save(force_insert, force_update, using, update_fields)
        if is_add:
            # 新規の場合、解約対象の車室とそのプロセスも新規追加する。
            if self.is_all:
                parking_positions = ParkingPosition.objects.public_filter(parking_lot=self.parking_lot)
            else:
                parking_positions = ParkingPosition.objects.public_filter(pk__in=self.parking_positions.split(','))
            for parking_position in parking_positions:
                contract = parking_position.get_current_contract()
                ParkingPositionCancellation.objects.create(
                    cancellation=self,
                    parking_lot=self.parking_lot,
                    parking_position=parking_position,
                    contract=contract,
                    contractor=contract.contractor,
                )


class ParkingPositionCancellation(BaseModel):
    cancellation = models.ForeignKey(ParkingLotCancellation)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室")
    contract = models.OneToOneField(Contract, on_delete=models.PROTECT, verbose_name="契約情報")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
    replacement = models.CharField(max_length=100, blank=True, null=True, verbose_name="代替駐車場")
    processes = GenericRelation('Process', related_query_name='parking_position_cancellations')

    class Meta:
        db_table = 'ap_parking_position_cancellation'
        verbose_name = "車室解約"
        verbose_name_plural = "車室解約一覧"

    def __str__(self):
        return '%s-%s' % (str(self.cancellation), str(self.parking_position))

    @cached_property
    def process(self):
        """解約のプロセスを取得する。

        :return:
        """
        return self.processes.first()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ParkingPositionCancellation, self).save(force_insert, force_update, using, update_fields)
        # 解約のプロセスを作成
        name = '33' if self.cancellation.is_with_continue else '32'
        Process.objects.create(name=name, content_object=self)


class PriceRaising(BaseModel):
    year = models.CharField(max_length=4, verbose_name="更新年")
    month = models.CharField(max_length=2, verbose_name="更新月")
    contract = models.OneToOneField(Contract, on_delete=models.PROTECT, verbose_name="契約情報")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    car = models.ForeignKey(ContractorCar, blank=True, null=True, verbose_name="契約する車")
    staff = models.ForeignKey(Member, verbose_name="担当者")
    start_date = models.DateField(verbose_name="契約開始日")
    end_date = models.DateField(verbose_name="契約終了日")
    current_amount = models.IntegerField(verbose_name="通常月請求税別額")
    current_amount_with_tax = models.IntegerField(verbose_name="通常月請求税込額")
    prev_amount = models.IntegerField(verbose_name="通常月請求税別額・更新前")
    prev_amount_with_tax = models.IntegerField(verbose_name="通常月請求税込額・更新前")
    reference_amount = models.IntegerField(blank=True, null=True, verbose_name="目安（税別）")
    leasing_amount = models.IntegerField(blank=True, null=True, verbose_name="リーシング担当者の値付（税別）")
    new_amount = models.IntegerField(blank=True, null=True, verbose_name="決定賃料（税別）")

    class Meta:
        db_table = 'ap_price_raising'
        verbose_name = "値上げ賃料設定"
        verbose_name_plural = "値上げ賃料設定"

    def __str__(self):
        return str(self.contractor)


class ContactHistory(BaseModel):
    contact_date = models.DateField(default=timezone.now, verbose_name="連絡日")
    contact_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="連絡者")
    content = models.CharField(max_length=255, verbose_name="連絡内容")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考・特記")

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'ap_contact_history'
        verbose_name = "連絡履歴"
        verbose_name_plural = "連絡履歴"

    def __str__(self):
        return self.content[:10] + "..." if len(str(self.content)) > 10 else self.content

    def get_contact_user_name(self):
        """連絡者の名前を取得する。

        :return:
        """
        if self.contact_user.first_name or self.contact_user.last_name:
            return '%s %s' % ((self.contact_user.last_name or ''), (self.contact_user.first_name or ''))
        else:
            return self.contact_user.username


class VPriceRaise(BaseViewModel):
    year = models.CharField(max_length=4, verbose_name="更新年")
    month = models.CharField(max_length=2, verbose_name="更新月")
    contract = models.OneToOneField(Contract, on_delete=models.DO_NOTHING, verbose_name="契約情報")
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, verbose_name="契約者")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.DO_NOTHING, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.DO_NOTHING, verbose_name="車室番号")
    car = models.ForeignKey(ContractorCar, blank=True, null=True, verbose_name="契約する車")
    staff = models.ForeignKey(Member, verbose_name="担当者")
    start_date = models.DateField(verbose_name="契約開始日")
    end_date = models.DateField(verbose_name="契約終了日")
    amount = models.IntegerField(verbose_name="通常月請求税別額")
    amount_with_tax = models.IntegerField(verbose_name="通常月請求税込額")
    prev_amount = models.IntegerField(verbose_name="通常月請求税別額・更新前")
    prev_amount_with_tax = models.IntegerField(verbose_name="通常月請求税込額・更新前")
    is_defect = models.BooleanField(verbose_name="駐車場設備不具合")
    around_price = models.IntegerField(blank=True, null=True, verbose_name="周辺相場")
    is_raise = models.BooleanField(verbose_name="対象内")

    class Meta:
        managed = False
        db_table = 'v_price_raise'
        verbose_name = "値上げ対象"
        verbose_name_plural = "値上げ対象一覧"

    def __str__(self):
        return str(self.contractor)


# class Trouble(BaseModel):
#     reception = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='trouble_reception_set', verbose_name="受付者")
#     staff = models.ForeignKey(Member, blank=True, null=True, on_delete=models.PROTECT, related_name='trouble_staff_set', verbose_name="対応者")
#     parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")


class VContractedParkingLot(BaseViewModel):
    code = models.IntegerField(primary_key=True, verbose_name="コード")
    name = models.CharField(max_length=100, verbose_name="駐車場名称")
    category = models.ForeignKey(ParkingLotType, on_delete=models.DO_NOTHING, verbose_name="分類")
    staff = models.ForeignKey(Member, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="担当者")
    post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name="郵便番号",
                                 validators=(RegexValidator(regex=constants.REG_POST_CODE),))
    address = models.CharField(max_length=255, blank=True, null=True, editable=False, verbose_name="所在地")
    owner = models.CharField(max_length=50, blank=True, null=True, verbose_name="所有者")
    lender = models.CharField(max_length=50, blank=True, null=True, verbose_name="貸主")
    lease_management_company = models.ForeignKey(
        LeaseManagementCompany, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="賃貸管理会社"
    )
    building_management_company = models.ForeignKey(
        BuildingManagementCompany, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="建物管理会社"
    )
    position_count = models.IntegerField(default=0, editable=False, verbose_name="車室数")
    contract_count = models.IntegerField(default=0, editable=False, verbose_name="契約数")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.DO_NOTHING, verbose_name="駐車場")
    # parking_lot_cancellation = models.ForeignKey(ParkingLotCancellation, blank=True, null=True,
    #                                              on_delete=models.DO_NOTHING, verbose_name="物件解約")
    # is_all_cancellation = models.BooleanField(default=False, verbose_name="全件解約")
    cancellation_count = models.IntegerField(default=0, editable=False, verbose_name="解約数")

    class Meta:
        managed = False
        db_table = 'v_contracted_parking_lot'
        verbose_name = "契約物件"
        verbose_name_plural = "契約物件一覧"

    def __str__(self):
        return self.name

    def get_cancellation_positions(self):
        if self.cancellation_count == self.position_count:
            return list()
        if self.cancellation_count:
            positions = [cancellation.parking_position.pk for cancellation in
                         ParkingPositionCancellation.objects.public_filter(parking_lot=self.parking_lot)]
            return self.parking_lot.parkingposition_set.exclude(pk__in=positions)
        else:
            return self.parking_lot.parkingposition_set.all()
