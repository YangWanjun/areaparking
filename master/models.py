# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from utils.django_base import BaseModel
from utils import constants, common

logger = common.get_ap_logger()


# Create your models here.
class Config(BaseModel):
    group = models.CharField(max_length=50, blank=False, null=True, verbose_name=u"グループ")
    name = models.CharField(max_length=50, unique=True, verbose_name=u"設定名")
    value = models.CharField(max_length=2000, verbose_name=u"設定値")
    comment = models.TextField(max_length=255, blank=True, null=True, verbose_name=u"備考")

    class Meta:
        ordering = ['group', 'name']
        verbose_name = verbose_name_plural = u"システム設定"
        db_table = 'mst_config'

    def __str__(self):
        return self.name

    @classmethod
    def get_circle_radius(cls):
        """地図時で円作成時の半径を取得する。

        取得失敗の場合はデフォルトの2000メートルを返却する。

        :return:
        """
        default = 2000
        try:
            circle = Config.objects.get(name=constants.CONFIG_CIRCLE_RADIUS)
            try:
                return int(circle)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_CIRCLE_RADIUS,
                                  value=default)
            return default


class Company(BaseModel):
    name = models.CharField(unique=True, max_length=30, verbose_name=u"会社名")
    kana = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"フリカナ")
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
    post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    email = models.EmailField(blank=True, null=True, verbose_name="メール")

    class Meta:
        db_table = 'ap_company'
        verbose_name = verbose_name_plural = "自社情報"

    def __str__(self):
        return self.name

    @classmethod
    def get_company(cls):
        """自社情報を取得する。

        :return:
        """
        return Company.objects.public_all().first()


class CarMaker(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="メーカー")

    class Meta:
        db_table = 'mst_car_maker'
        ordering = ['name']
        verbose_name = "メーカー"
        verbose_name_plural = "メーカー一覧"

    def __str__(self):
        return self.name


class CarModel(BaseModel):
    maker = models.ForeignKey(CarMaker, on_delete=models.PROTECT, verbose_name="メーカー")
    name = models.CharField(max_length=100, verbose_name="車種")
    grade_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="グレード名")
    sale_date = models.DateField(blank=True, null=True, verbose_name="発売年度")
    length = models.IntegerField(blank=False, null=True, verbose_name="全長")
    width = models.IntegerField(blank=False, null=True, verbose_name="全幅")
    height = models.IntegerField(blank=False, null=True, verbose_name="全高")
    weight = models.IntegerField(blank=False, null=True, verbose_name="重量")
    f_value = models.IntegerField(blank=False, null=True, verbose_name="F値")
    r_value = models.IntegerField(blank=False, null=True, verbose_name="R値")
    min_height = models.IntegerField(blank=False, null=True, verbose_name="ﾒｰｶｰの地上最低高")

    class Meta:
        db_table = 'mst_car_model'
        ordering = ['name']
        unique_together = ('maker', 'name', 'grade_name')
        verbose_name = "車種"
        verbose_name_plural = "車種一覧"

    def __str__(self):
        if self.grade_name:
            return '%s - %s ' % (self.name, self.grade_name)
        else:
            return self.name


class Bank(BaseModel):
    code = models.CharField(max_length=4, verbose_name="金融機関コード")
    name = models.CharField(max_length=30, verbose_name="金融機関名称")
    kana = models.CharField(max_length=30, verbose_name="金融機関カナ")

    class Meta:
        db_table = 'mst_bank'
        ordering = ['code']
        verbose_name = "金融機関"
        verbose_name_plural = "金融機関一覧"

    def __str__(self):
        return self.name


class BankAccount(BaseModel):
    bank = models.ForeignKey(Bank, verbose_name=u"銀行")
    branch_no = models.CharField(max_length=7, verbose_name=u"支店番号")
    branch_name = models.CharField(max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(max_length=1, choices=constants.CHOICE_BANK_ACCOUNT_TYPE, verbose_name=u"預金種類")
    account_number = models.CharField(max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")

    class Meta:
        db_table = 'mst_bank_account'
        ordering = ['bank', 'branch_no']
        unique_together = ('branch_no', 'account_number')
        verbose_name = "銀行口座"
        verbose_name_plural = "銀行口座一覧"

    def __str__(self):
        return self.branch_no


class TransmissionRoute(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="名称")

    class Meta:
        db_table = 'mst_transmission_route'
        ordering = ['name']
        verbose_name = "媒体"
        verbose_name_plural = "媒体一覧"

    def __str__(self):
        return self.name


class Mediation(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="業者名称")

    class Meta:
        db_table = 'mst_mediation'
        ordering = ['name']
        verbose_name = "仲介業者"
        verbose_name_plural = "仲介業者一覧"

    def __str__(self):
        return self.name


class Payment(BaseModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="入金項目")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'mst_payment'
        ordering = ['name']
        verbose_name = "入金項目"
        verbose_name_plural = "入金項目一覧"

    def __str__(self):
        return self.name


class ReportFormat(BaseModel):
    path = models.FileField(upload_to=common.get_parking_lot_doc_path)
    kbn = models.CharField(max_length=3, choices=constants.CHOICE_REPORT_KBN, verbose_name="帳票区分")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
    order = models.SmallIntegerField(editable=False, verbose_name="並び順")

    class Meta:
        db_table = 'mst_report_format'
        ordering = ['kbn']
        verbose_name = "帳票フォーマット"
        verbose_name_plural = "帳票フォーマット一覧"

    def __str__(self):
        return os.path.basename(str(self.path))


class MailTemplate(BaseModel):
    title = models.CharField(max_length=50, unique=True, verbose_name=u"送信メールのタイトル")
    body = models.TextField(blank=True, null=True, verbose_name=u"メール本文(Plain Text)")
    password = models.TextField(blank=True, null=True, verbose_name=u"パスワードお知らせ本文(Plain Text)")
    comment = models.TextField(max_length=255, blank=True, null=True, verbose_name=u"説明")

    class Meta:
        db_table = 'mst_mail_template'
        ordering = ['title']
        verbose_name = verbose_name_plural = u"メールテンプレート"

    def __str__(self):
        return self.title


class MailGroup(BaseModel):
    code = models.CharField(max_length=3, primary_key=True, choices=constants.CHOICE_MAIL_GROUP, verbose_name=u"コード")
    name = models.CharField(max_length=50, blank=False, null=True, verbose_name=u"名称")
    sender = models.EmailField(verbose_name=u"メール差出人")
    template = models.ForeignKey(MailTemplate, on_delete=models.PROTECT,
                                 verbose_name=u"メールテンプレート")

    class Meta:
        db_table = 'mst_mail_group'
        ordering = ['code']
        verbose_name = verbose_name_plural = u"メールグループ"

    def __str__(self):
        return self.name

    def get_cc_list(self):
        """メール送信時のＣＣ一覧を取得する。

        :return:
        """
        return MailCcList.objects.public_filter(group=self, is_bcc=False)

    def get_bcc_list(self):
        """メール送信時のＢＣＣ一覧を取得する。

        :return:
        """
        return MailCcList.objects.public_filter(group=self, is_bcc=True)


class MailCcList(BaseModel):
    group = models.ForeignKey(MailGroup, on_delete=models.PROTECT, verbose_name=u"メールグループ")
    email = models.EmailField(verbose_name=u"メールアドレス")
    is_bcc = models.BooleanField(default=False, verbose_name="ＢＣＣ")

    class Meta:
        db_table = 'mst_mail_cc'
        ordering = ['group', 'email']
        verbose_name = verbose_name_plural = u"メールＣＣリスト"

    def __str__(self):
        return self.email
