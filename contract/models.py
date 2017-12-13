# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core. validators import RegexValidator

from utils.django_base import BaseModel
from utils import constants

from parkinglot.models import ParkingLot, ParkingPosition
from employee.models import Member
from master.models import Mediation, BankAccount, CarMaker, Payment


# Create your models here.
class BaseContractor(BaseModel):
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
    corporate_staff_department = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者所属")
    corporate_staff_position = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者役職")
    corporate_extension = models.CharField(max_length=10, blank=True, null=True, verbose_name="内線番号")
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

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseContract(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    contractor = models.ForeignKey('Contractor', on_delete=models.PROTECT, verbose_name="契約者")
    # 基本情報
    contract_no = models.CharField(max_length=20, verbose_name="契約番号")
    contract_date = models.DateField(verbose_name="契約日")
    start_date = models.DateField(verbose_name="契約開始日")
    end_date = models.DateField(verbose_name="契約終了日")
    pay_date = models.DateField(blank=True, null=True, verbose_name="賃料発生日",
                                help_text="未入力の場合、契約期間の開始日が賃料発生日として扱われます")
    notify_start_date = models.DateField(blank=True, null=True, verbose_name="契約終了通知開始日")
    notify_end_date = models.DateField(blank=True, null=True, verbose_name="契約終了通知終了日")
    staff = models.ForeignKey(Member, verbose_name="担当者")
    mediation = models.ForeignKey(Mediation, verbose_name="仲介業者")
    staff_proxy = models.ForeignKey(Member, null=True, blank=True, related_name='contract_proxy_set',
                                    verbose_name="宅建取引士")
    # 口座情報
    payee_bank_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.PROTECT,
                                           verbose_name="振込先口座")
    # 車情報
    car_maker = models.ForeignKey(CarMaker, verbose_name="車メーカー")
    car_model = models.CharField(max_length=100, verbose_name="車種")
    car_color = models.CharField(max_length=10, blank=True, null=True, verbose_name="色")
    car_no = models.CharField(max_length=20, blank=True, null=True, verbose_name="No.プレート")
    car_comment = models.CharField(max_length=200, blank=True, null=True, verbose_name="車の備考")

    class Meta:
        abstract = True

    def __str__(self):
        return '%s（%s～%s）' % (str(self.contractor), self.start_date, self.end_date)


class Contractor(BaseContractor):
    code = models.IntegerField(
        primary_key=True, verbose_name="契約者No.",
        validators=(RegexValidator(regex=r'^\d{1,8}$'),)
    )

    class Meta:
        db_table = 'ap_contractor'
        ordering = ['name']
        verbose_name = "契約者"
        verbose_name_plural = "契約者一覧"


class Contract(BaseContract):

    class Meta:
        db_table = 'ap_contract'
        ordering = ['contractor', 'start_date']
        verbose_name = "契約情報"
        verbose_name_plural = "契約情報一覧"


class ContractPayment(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, verbose_name="契約情報")
    pay_timing = models.CharField(max_length=2, choices=constants.CHOICE_PAY_TIMING, verbose_name="タイミング")
    payment = models.ForeignKey(Payment, verbose_name="入金項目")
    amount = models.IntegerField(verbose_name="請求額")
    consumption_tax = models.IntegerField(verbose_name="消費税")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_contract_payment'
        ordering = ['contract', 'pay_timing']
        verbose_name = "入金項目"
        verbose_name_plural = "入金項目一覧"

    def __str__(self):
        return '%s：%s' % (str(self.contract), self.payment)


class TempContractor(BaseContractor):

    class Meta:
        db_table = 'ap_temp_contractor'
        ordering = ['name']
        verbose_name = "仮契約者"
        verbose_name_plural = "仮契約者一覧"


class TempContract(BaseContract):
    contractor = models.ForeignKey(TempContractor, on_delete=models.PROTECT, verbose_name="仮契約者")
    # 基本情報
    contract_no = models.CharField(blank=True, null=True, max_length=20, verbose_name="契約番号")
    contract_date = models.DateField(blank=True, null=True, verbose_name="契約日")
    start_date = models.DateField(blank=True, null=True, verbose_name="契約開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name="契約終了日")
    pay_date = models.DateField(blank=True, null=True, verbose_name="賃料発生日",
                                help_text="未入力の場合、契約期間の開始日が賃料発生日として扱われます")
    notify_start_date = models.DateField(blank=True, null=True, verbose_name="契約終了通知開始日")
    notify_end_date = models.DateField(blank=True, null=True, verbose_name="契約終了通知終了日")
    staff = models.ForeignKey(Member, blank=True, null=True, verbose_name="担当者")
    mediation = models.ForeignKey(Mediation, blank=True, null=True, verbose_name="仲介業者")
    staff_proxy = models.ForeignKey(Member, null=True, blank=True, related_name='temp_contract_proxy_set',
                                    verbose_name="宅建取引士")
    # 口座情報
    payee_bank_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.PROTECT,
                                           verbose_name="振込先口座")
    # 車情報
    car_maker = models.ForeignKey(CarMaker, blank=True, null=True, verbose_name="車メーカー")
    car_model = models.CharField(max_length=100, blank=True, null=True, verbose_name="車種")
    car_color = models.CharField(max_length=10, blank=True, null=True, verbose_name="色")
    car_no = models.CharField(max_length=20, blank=True, null=True, verbose_name="No.プレート")
    car_comment = models.CharField(max_length=200, blank=True, null=True, verbose_name="車の備考")

    class Meta:
        db_table = 'ap_temp_contract'
        ordering = ['contractor', 'start_date']
        verbose_name = "仮契約情報"
        verbose_name_plural = "仮契約情報一覧"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(TempContract, self).save(force_insert, force_update, using, update_fields)
        # 進捗のプロセス作成
        process = ContractProcess.objects.create(temp_contract=self)
        # 申込書送付のタスク
        Task.objects.create(process=process, order=1, name='申込書送付')
        # 申込書確認のタスク
        Task.objects.create(process=process, order=2, name='申込書確認')
        # 住所・電話番号 審査・確認のタスク
        Task.objects.create(process=process, order=3, name='住所・電話番号 審査・確認')
        # 勤め先審査のタスク
        Task.objects.create(process=process, order=4, name='勤め先審査')
        # 車両サイズ審査のタスク
        Task.objects.create(process=process, order=5, name='車両サイズ審査')
        # 申込ルート元審査のタスク
        Task.objects.create(process=process, order=6, name='申込ルート元審査')
        # 契約書類一式の送付のタスク
        Task.objects.create(process=process, order=7, name='契約書類一式の送付')
        # 入金確認のタスク
        Task.objects.create(process=process, order=8, name='入金確認')
        # 契約完了のタスク
        Task.objects.create(process=process, order=9, name='契約完了')


class ContractProcess(BaseModel):
    temp_contract = models.OneToOneField(TempContract, related_name='process', verbose_name="仮契約")

    class Meta:
        db_table = 'ap_contract_process'
        ordering = ['temp_contract']
        verbose_name = "契約進捗"
        verbose_name_plural = "契約進捗一覧"

    def get_percent(self):
        """進捗の完成度（%）を取得

        :return:
        """
        finished = Task.objects.public_filter(process=self, status__in=['10', '99']).count()
        total = Task.objects.public_filter(process=self).count()
        return round(finished / total, 3) * 100 if total else 0.0


class Task(BaseModel):
    process = models.ForeignKey(ContractProcess, verbose_name="契約進捗")
    name = models.CharField(max_length=50, verbose_name="タスク名称")
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_TASK_STATUS, verbose_name='ステータス')
    order = models.SmallIntegerField(verbose_name="並び順")
    is_end = models.BooleanField(default=False, verbose_name="終了タスク")

    class Meta:
        db_table = 'ap_task'
        ordering = ['process', 'order']
        verbose_name = "タスク"
        verbose_name_plural = "タスク一覧"
