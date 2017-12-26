# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from django.template import Context, Template

from utils import constants, common
from utils.django_base import BaseModel, PublicManager

from parkinglot.models import ParkingLot, ParkingPosition
from employee.models import Member
from format.models import ReportFile
from master.models import Mediation, BankAccount, Config, Payment, MailGroup, TransmissionRoute
from utils.app_base import get_total_context, get_user_subscription_url, get_signed_value


# Create your models here.
class Contractor(BaseModel):
    code = models.AutoField(primary_key=True, verbose_name="契約者No.")
    category = models.CharField(max_length=1, choices=constants.CHOICE_CONTRACTOR_TYPE, verbose_name="契約者分類")
    name = models.CharField(max_length=15, verbose_name="名前")
    kana = models.CharField(max_length=15, blank=True, null=True, verbose_name="カナ")
    post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name="郵便番号",
                                 validators=(RegexValidator(regex=constants.REG_POST_CODE),))
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
    # 個人情報
    personal_gender = models.CharField(max_length=1, blank=True, null=True, choices=constants.CHOICE_GENDER,
                                       verbose_name="性別")
    personal_birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")
    # 法人情報
    corporate_business_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="業種／事業")
    corporate_web_site = models.URLField(blank=True, null=True, verbose_name="ホームページ")
    corporate_president = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"代表者名")
    corporate_staff_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"担当者名")
    corporate_staff_kana = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"担当者カナ")
    # corporate_staff_email = models.EmailField(blank=True, null=True, verbose_name="担当者Email")
    # corporate_staff_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"担当者電話番号")
    # corporate_staff_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"担当者ファックス")
    corporate_staff_phone = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"担当者携帯電話")
    corporate_staff_department = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者所属")
    corporate_staff_position = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者役職")
    corporate_capital = models.IntegerField(blank=True, null=True, verbose_name="資本金")
    corporate_turnover = models.IntegerField(blank=True, null=True, verbose_name="年収／年商")
    # 勤務先
    workplace_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="勤務先名称")
    workplace_post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"勤務先郵便番号")
    workplace_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"勤務先住所１")
    workplace_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"勤務先住所２")
    workplace_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"勤務先電話番号")
    workplace_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"勤務先ファックス")
    # 連絡先
    contact_name = models.CharField(max_length=15, blank=True, null=True, verbose_name="連絡先名称")
    contact_kana = models.CharField(max_length=15, blank=True, null=True, verbose_name="連絡先カナ")
    contact_post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"連絡先郵便番号")
    contact_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"連絡先住所１")
    contact_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"連絡先住所２")
    contact_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"連絡先電話番号")
    contact_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"連絡先ファックス")
    contact_relation = models.CharField(max_length=20, blank=True, null=True, verbose_name="連絡先との間柄")
    # 書類送付先
    delivery_type = models.CharField(max_length=2, blank=True, null=True,
                                     choices=constants.CHOICE_PAPER_DELIVERY_TYPE, verbose_name="書類送付先区分")
    delivery_honorific = models.CharField(max_length=1, blank=True, null=True,
                                          choices=constants.CHOICE_HONORIFIC, verbose_name="宛名敬称")
    delivery_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="送付先名称")
    delivery_kana = models.CharField(max_length=30, blank=True, null=True, verbose_name="送付先カナ")
    delivery_post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"送付先郵便番号")
    delivery_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"送付先住所１")
    delivery_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"送付先住所２")
    delivery_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"送付先電話番号")
    delivery_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"送付先ファックス")
    # 保証人
    guarantor_name = models.CharField(max_length=15, blank=True, null=True, verbose_name="保証人名称")
    guarantor_kana = models.CharField(max_length=15, blank=True, null=True, verbose_name="保証人カナ")
    guarantor_birthday = models.DateField(blank=True, null=True, verbose_name="保証人生年月日")
    guarantor_post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"保証人郵便番号")
    guarantor_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"保証人住所１")
    guarantor_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"保証人住所２")
    guarantor_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"保証人電話番号")
    guarantor_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"保証人ファックス")
    guarantor_relation = models.CharField(max_length=20, blank=True, null=True, verbose_name="保証人との間柄")
    guarantor_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
    # 仮契約であるかどうかのステータス
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_CONTRACT_STATUS, editable=False,
                              verbose_name="ステータス")

    objects = PublicManager(is_deleted=False)
    temp_objects = PublicManager(is_deleted=False, status='01')
    real_objects = PublicManager(is_deleted=False, status='11')

    class Meta:
        db_table = 'ap_contractor'
        ordering = ['name']
        verbose_name = "契約者"
        verbose_name_plural = "契約者一覧"

    def __str__(self):
        return self.name


class ContractorCar(BaseModel):
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
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

    class Meta:
        db_table = 'ap_contractor_car'
        ordering = ['contractor', 'car_maker', 'car_model']
        verbose_name = "保有車"
        verbose_name_plural = "保有車一覧"

    def __str__(self):
        return self.car_model


class Contract(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
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
        return '%s（%s～%s）' % (str(self.contractor), self.start_date, self.end_date)

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

    def get_suitable_positions(self):
        """駐車可能の車室を取得する

        :return:
        """
        positions = self.parking_lot.get_suitable_positions(self.car.car_length, self.car.car_width,
                                                            self.car.car_height,
                                                            self.car.car_weight)
        return positions

    def get_contract_process(self):
        """ユーザー申込みから成約までのプロセスを取得する。

        :return:
        """
        return self.processes.filter(name='01').first()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_new = True if self.pk is None else False
        super(Contract, self).save(force_insert, force_update, using, update_fields)
        if is_new:
            # 進捗のプロセス作成
            process = Process.objects.create(name='01', content_object=self)
            for i, category in enumerate(constants.CHOICE_TASK_CATEGORY, 1):
                task = Task(process=process, order=i, category=category[0], name=category[1])
                if i == len(constants.CHOICE_TASK_CATEGORY):
                    task.is_end = True
                task.save()
            # 入金項目作成
            payments = Payment.objects.public_filter(is_active=True)
            consumption_tax_rate = Config.get_consumption_tax_rate()
            decimal_type = Config.get_decimal_type()
            for payment in payments:
                contract_payment = ContractPayment(contract=self, timing=payment.timing, payment=payment)
                contract_payment.amount = payment.amount or 0
                if payment.timing == '11':
                    # 契約開始月
                    contract_payment.amount = self.get_current_month_price()
                elif payment.timing == '30':
                    contract_payment.amount = self.get_monthly_price()
                contract_payment.consumption_tax = common.get_integer(contract_payment.amount * consumption_tax_rate,
                                                                      decimal_type)
                contract_payment.save()


class ContractPayment(BaseModel):
    contract = models.ForeignKey(Contract, verbose_name="契約情報")
    timing = models.CharField(max_length=2, choices=constants.CHOICE_PAY_TIMING, verbose_name="タイミング")
    payment = models.ForeignKey(Payment, verbose_name="入金項目")
    amount = models.IntegerField(verbose_name="請求額")
    consumption_tax = models.IntegerField(verbose_name="消費税")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_contract_payment'
        ordering = ['contract', 'timing']
        verbose_name = "入金項目"
        verbose_name_plural = "入金項目一覧"

    def __str__(self):
        return '%s：%s' % (str(self.contract), self.payment)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.consumption_tax = self.payment.get_consumption_tax()
        super(ContractPayment, self).save(force_insert, force_update, using, update_fields)


class Process(BaseModel):
    name = models.CharField(max_length=2, choices=constants.CHOICE_PROCESS)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'ap_process'
        unique_together = ['name', 'content_type', 'object_id']
        verbose_name = "進捗"
        verbose_name_plural = "進捗一覧"

    def get_percent(self):
        """進捗の完成度（%）を取得

        :return:
        """
        finished = Task.objects.public_filter(process=self, status__in=['10', '99']).count()
        total = Task.objects.public_filter(process=self).count()
        return ('%.1f' % (round(finished / total, 3) * 100,)) if total else 0.0


class Task(BaseModel):
    process = models.ForeignKey(Process, verbose_name="契約進捗")
    category = models.CharField(max_length=3, choices=constants.CHOICE_TASK_CATEGORY, verbose_name="タスク名称")
    name = models.CharField(max_length=50, verbose_name="タスク名称")
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_TASK_STATUS, verbose_name='ステータス')
    updated_user = models.ForeignKey(User, blank=True, null=True, verbose_name="更新ユーザー")
    url_links = models.CharField(max_length=2000, blank=True, null=True, verbose_name="リンク")
    reports = GenericRelation(ReportFile, related_query_name='subscriptions')
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
        if self.category == '010':
            # 申込書送付
            group = MailGroup.get_subscription_mail_info()
            return group
        return None

    def get_mail_template(self):
        group = self.get_mail_group()
        if group:
            t_title = Template(group.template.title)
            t_body = Template(group.template.body)
            t_password = Template(group.template.password) if group.template.password else None
            comment = group.template.comment or ''
            context = Context(get_total_context(
                parking_lot=self.process.content_object.parking_lot,
                contractor=self.process.content_object.contractor,
            ))
            context.update(get_user_subscription_url(self))

            return {
                'title': t_title.render(context),
                'body': t_body.render(context),
                'password': t_password.render(context) if t_password else '',
                'comment': comment,
            }
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

    def get_signed_pk(self):
        return get_signed_value(self.pk)

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


class TempContract(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING, verbose_name="契約情報")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.DO_NOTHING, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.DO_NOTHING, verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, verbose_name="契約者")
    percent = models.DecimalField(max_digits=4, decimal_places=1, editable=False, verbose_name="進捗")
    # 基本情報
    contract_date = models.DateField(blank=True, null=True, verbose_name="契約日")
    start_date = models.DateField(blank=True, null=True, verbose_name="契約開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name="契約終了日")
    staff = models.ForeignKey(Member, on_delete=models.DO_NOTHING, verbose_name="担当者")
    mediation = models.ForeignKey(Mediation, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="仲介業者")
    staff_assistant1 = models.ForeignKey(Member, null=True, blank=True, related_name='temp_contract_assistant1_set',
                                         on_delete=models.DO_NOTHING, verbose_name="アシスタント１")
    staff_assistant2 = models.ForeignKey(Member, null=True, blank=True, related_name='temp_contract_assistant2_set',
                                         on_delete=models.DO_NOTHING, verbose_name="アシスタント２")
    staff_assistant3 = models.ForeignKey(Member, null=True, blank=True, related_name='temp_contract_assistant3_set',
                                         on_delete=models.DO_NOTHING, verbose_name="アシスタント３")
    # 口座情報
    payee_bank_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.DO_NOTHING,
                                           verbose_name="振込先口座")
    # 車情報
    car = models.ForeignKey(ContractorCar, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="契約車")

    class Meta:
        managed = False
        db_table = 'v_temp_contract'
        ordering = ['contractor', 'start_date']
        verbose_name = "仮契約情報"
        verbose_name_plural = "仮契約情報一覧"

    def __str__(self):
        return '%s（%s～%s）' % (str(self.contractor), self.start_date, self.end_date)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super(TempContract, self).save(force_insert, force_update, using, update_fields)


class Cancellation(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING, verbose_name="契約情報")

