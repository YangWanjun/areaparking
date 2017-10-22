# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core. validators import RegexValidator

from utils.django_base import BaseModel
from utils import constants


# Create your models here.
class Contractor(BaseModel):
    number = models.IntegerField(
        verbose_name="契約者No.", unique=True,
        validators=(RegexValidator(regex=r'^\d{8}$'),)
    )
    name = models.CharField(max_length=15, verbose_name="名前")
    kana = models.CharField(max_length=15, verbose_name="カナ")
    segment = models.CharField(max_length=1, choices=constants.CHOICE_CONTRACTOR_TYPE, verbose_name="契約者分類")
    # 個人情報
    gender = models.CharField(max_length=1, choices=constants.CHOICE_GENDER, verbose_name="性別")
    personal_post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    personal_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    personal_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    personal_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    personal_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")
    personal_email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    personal_birthday = models.DateField(blank=True, null=True, verbose_name="生年月日", help_text="法人の場合は設立年月日")
    personal_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
    # 法人情報
    web_site = models.URLField(blank=True, null=True, verbose_name="ホームページ")
    business_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="業種／事業")
    president = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"代表者名")
    staff_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"担当者名")
    staff_department = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者所属")
    position = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者役職")
    extension = models.CharField(max_length=10, blank=True, null=True, verbose_name="内線番号")
    capital = models.IntegerField(blank=True, null=True, verbose_name="資本金")
    turnover = models.IntegerField(blank=True, null=True, verbose_name="年収／年商")
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
    paper_delivery_type = models.CharField(max_length=2, blank=True, null=True,
                                           choices=constants.CHOICE_PAPER_DELIVERY_TYPE, verbose_name="書類送付先区分")
    honorific = models.CharField(max_length=1, blank=True, null=True,
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
