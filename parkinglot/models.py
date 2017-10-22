# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime

from django.db import models
from django.core. validators import RegexValidator

from master.models import ParkingLotType, ParkingTimeLimit
from utils.django_base import BaseModel


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


class ParkingLot(BaseModel):
    number = models.IntegerField(
        verbose_name="駐車場No.", unique=True,
        validators=(RegexValidator(regex=r'^\d{8}$'),)
    )
    name = models.CharField(max_length=100, verbose_name="駐車場名称")
    kana = models.CharField(max_length=100, blank=True, null=True, verbose_name="駐車場カナ")
    segment = models.ForeignKey(ParkingLotType)
    pref_code = models.CharField(max_length=2, verbose_name="都道府県コード")
    pref_name = models.CharField(max_length=15,verbose_name="都道府県名称")
    city_code = models.CharField(max_length=2, verbose_name="市区町村コード")
    city_name = models.CharField(max_length=15,verbose_name="市区町村名称")
    town_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="町域名称")
    aza_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="丁番地")
    other_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="その他")
    lon = models.FloatField(blank=True, null=True, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, verbose_name="緯度")
    # contract_period = models.IntegerField(
    #     default=2, verbose_name="新規契約を作成した際、この初期値で契約期間が自動入力されます。"
    # )
    post_code = models.CharField(
        blank=True, null=True, max_length=7, verbose_name="郵便番号")
    traffic = models.CharField(max_length=200, verbose_name="交通")
    car_count = models.IntegerField(default=0, verbose_name="駐車台数")
    bike_count = models.IntegerField(default=0, verbose_name="駐輪台数")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot'
        ordering = ['number']
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __unicode__(self):
        return self.name


class ParkingLotImage(BaseModel):
    parking_plot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    image = models.ImageField(upload_to='images/parking')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_image'
        verbose_name = "駐車場画像"
        verbose_name_plural = "駐車場画像一覧"

    def __unicode__(self):
        return self.image

    def get_image_path(self, filename):
        prefix = 'images/'
        name = '{}_{}'.format(self.parking_plot.name, datetime.datetime.now().strftime('%y%m%d%H%M%S%f'))
        extension = os.path.splitext(filename)[-1]
        return prefix + name + extension


class ParkingPosition(BaseModel):
    parking_plot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    no = models.IntegerField(null=True, blank=True, verbose_name="車室No")
    length = models.IntegerField(default=0, verbose_name="全長")
    width = models.IntegerField(default=0, verbose_name="全幅")
    height = models.IntegerField(default=0, verbose_name="全高")
    weight = models.IntegerField(default=0, verbose_name="重量")
    tyre_width = models.IntegerField(default=0, verbose_name="ﾒｰｶｰのタイヤ幅")
    tyre_width_ap = models.IntegerField(default=0, verbose_name="AP計測のタイヤ幅")
    min_height = models.IntegerField(default=0, verbose_name="ﾒｰｶｰの地上最低高")
    f_value = models.IntegerField(blank=True, null=True, verbose_name="F値")
    r_value = models.IntegerField(blank=True, null=True, verbose_name="R値")
    time_limit = models.ForeignKey(ParkingTimeLimit, blank=True, null=True, verbose_name="時間制限")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot'
        ordering = ['number']
        verbose_name = "車室"
        verbose_name_plural = "車室一覧"

    def __unicode__(self):
        return self.no if self.no else unicode(self.parking_plot)
