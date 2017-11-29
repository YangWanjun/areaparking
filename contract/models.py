# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core. validators import RegexValidator

from utils.django_base import BaseModel
from utils import constants

from parkinglot.models import ParkingLot, ParkingPosition
from master import models as master_models


# Create your models here.
class Contractor(BaseModel):
    code = models.IntegerField(
        verbose_name="契約者No.", unique=True,
        validators=(RegexValidator(regex=r'^\d{1,8}$'),)
    )
    segment = models.CharField(max_length=1, choices=constants.CHOICE_CONTRACTOR_TYPE, verbose_name="契約者分類")
    name = models.CharField(max_length=15, verbose_name="名前")
    kana = models.CharField(max_length=15, blank=True, null=True, verbose_name="カナ")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
    # 個人情報
    personal_gender = models.CharField(max_length=1, blank=True, null=True, choices=constants.CHOICE_GENDER, verbose_name="性別")
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
        db_table = 'ap_contractor'
        ordering = ['name']
        verbose_name = "契約者"
        verbose_name_plural = "契約者一覧"

    def __str__(self):
        return self.name


class Contract(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
    contract_date = models.DateField(verbose_name="契約日")
    start_date = models.DateField(verbose_name="契約開始日")
    end_date = models.DateField(verbose_name="契約終了日")
    pay_date = models.DateField(blank=True, null=True, verbose_name="賃料発生日",
                                help_text="未入力の場合、契約期間の開始日が賃料発生日として扱われます")
    # 口座情報
    # bank = models.ForeignKey(master_models.Bank, blank=True, null=True, on_delete=models.PROTECT, verbose_name="振込先口座")

    class Meta:
        db_table = 'ap_contract'
        ordering = ['contractor', 'start_date']
        verbose_name = "契約情報"
        verbose_name_plural = "契約情報一覧"

    def __str__(self):
        return '%s（%s～%s）' % (str(self.contractor), self.start_date, self.end_date)


class TempContract(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
    contract_date = models.DateField(blank=True, null=True, verbose_name="契約日")
    start_date = models.DateField(blank=True, null=True, verbose_name="契約開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name="契約終了日")
    pay_date = models.DateField(blank=True, null=True, verbose_name="賃料発生日",
                                help_text="未入力の場合、契約期間の開始日が賃料発生日として扱われます")

    class Meta:
        db_table = 'ap_temp_contract'
        ordering = ['contractor', 'start_date']
        verbose_name = "仮契約情報"
        verbose_name_plural = "仮契約情報一覧"

    def __str__(self):
        return str(self.pk)
