# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core. validators import RegexValidator

from utils.django_base import BaseModel
from utils import constants


# Create your models here.
class Company(BaseModel):
    name = models.CharField(unique=True, max_length=30, verbose_name=u"会社名")
    kana = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"フリカナ")
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")

    class Meta:
        db_table = 'ap_company'
        verbose_name = verbose_name_plural = "自社情報"

    def __unicode__(self):
        return self.name


class ParkingLotType(BaseModel):
    code = models.IntegerField(primary_key=True, verbose_name="駐車場分類No.",
                                 validators=(RegexValidator(regex=r'^\d{1,4}$'),))
    name = models.CharField(max_length=30, verbose_name="名称")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'mst_parking_lot_type'
        ordering = ['code']
        verbose_name = "駐車場分類"
        verbose_name_plural = "駐車場分類一覧"

    def __unicode__(self):
        return self.name


class ParkingTimeLimit(BaseModel):
    name = models.CharField(max_length=30, verbose_name="名称")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'mst_parking_time_limit'
        ordering = ['name']
        verbose_name = "時間制限"
        verbose_name_plural = "時間制限一覧"

    def __unicode__(self):
        return self.name


class BankCode(BaseModel):
    code = models.CharField(max_length=4, verbose_name="金融機関コード")
    name = models.CharField(max_length=30, verbose_name="金融機関名称")
    kana = models.CharField(max_length=30, verbose_name="金融機関カナ")

    class Meta:
        db_table = 'mst_bank_code'
        ordering = ['code']
        verbose_name = "金融機関"
        verbose_name_plural = "金融機関一覧"

    def __unicode__(self):
        return self.name


class ManagementType(BaseModel):
    code = models.CharField(max_length=4, verbose_name="管理形態コード")
    name = models.CharField(max_length=30, verbose_name="管理形態名称")

    class Meta:
        db_table = 'mst_management_type'
        ordering = ['code']
        verbose_name = "管理形態"
        verbose_name_plural = "管理形態一覧"

    def __unicode__(self):
        return self.name


class CarMaker(BaseModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="メーカー")

    class Meta:
        db_table = 'mst_car_maker'
        ordering = ['name']
        verbose_name = "メーカー"
        verbose_name_plural = "メーカー一覧"

    def __unicode__(self):
        return self.name


class CarModel(BaseModel):
    maker = models.ForeignKey(CarMaker, on_delete=models.PROTECT, verbose_name="メーカー")
    name = models.CharField(max_length=50, verbose_name="車種")
    grade_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="グレード名")
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

    def __unicode__(self):
        return self.name


class Bank(BaseModel):
    bank_name = models.CharField(max_length=20, verbose_name=u"銀行名称")
    branch_no = models.CharField(max_length=7, verbose_name=u"支店番号")
    branch_name = models.CharField(max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(max_length=1, choices=constants.CHOICE_BANK_ACCOUNT_TYPE, verbose_name=u"預金種類")
    account_number = models.CharField(max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")

    class Meta:
        db_table = 'mst_bank'
        ordering = ['bank_name', 'branch_no']
        unique_together = ('branch_no', 'account_number')
        verbose_name = "銀行口座"
        verbose_name_plural = "銀行口座一覧"

    def __unicode__(self):
        return self.bank_name
