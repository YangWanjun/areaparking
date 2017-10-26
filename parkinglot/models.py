# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime

from django.db import models
from django.core. validators import RegexValidator

from master.models import ParkingLotType, ParkingTimeLimit, ManagementType
from utils.django_base import BaseModel


# Create your models here.
class Managerment(BaseModel):
    code = models.IntegerField(
        verbose_name="管理会社No.", unique=True,
        validators=(RegexValidator(regex=r'^\d{1,8}$'),)
    )
    segment = models.ForeignKey(ManagementType, verbose_name="駐車場分類")
    name = models.CharField(max_length=100, verbose_name="管理会社名称")
    kana = models.CharField(max_length=100, blank=True, null=True, verbose_name="管理会社カナ")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name="郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")


class ParkingLot(BaseModel):
    code = models.IntegerField(
        verbose_name="駐車場No.", unique=True,
        validators=(RegexValidator(regex=r'^\d{1,8}$'),)
    )
    name = models.CharField(max_length=100, verbose_name="駐車場名称")
    kana = models.CharField(max_length=100, blank=True, null=True, verbose_name="駐車場カナ")
    segment = models.ForeignKey(ParkingLotType, verbose_name="駐車場分類")
    pref_code = models.CharField(max_length=2, verbose_name="都道府県コード")
    pref_name = models.CharField(max_length=15,verbose_name="都道府県名称")
    city_code = models.CharField(max_length=5, verbose_name="市区町村コード")
    city_name = models.CharField(max_length=15,verbose_name="市区町村名称")
    town_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="町域名称")
    aza_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="丁番地")
    other_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="その他")
    lon = models.FloatField(blank=True, null=True, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, verbose_name="緯度")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name="郵便番号")
    traffic = models.CharField(max_length=200, blank=True, null=True, verbose_name="交通")
    car_count = models.IntegerField(default=0, verbose_name="駐車台数")
    bike_count = models.IntegerField(default=0, verbose_name="駐輪台数")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot'
        ordering = ['code']
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __unicode__(self):
        return self.name

    def address(self):
        return "{}{}{}{}{}".format(self.pref_name, self.city_name, self.town_name or '', self.aza_name or '', self.other_name or '')


def get_image_path(self, filename):
    prefix = 'images/'
    name = '{}_{}'.format(self.parking_lot.name, datetime.datetime.now().strftime('%y%m%d%H%M%S%f'))
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_doc_path(self, filename):
    prefix = 'docs/{}/'.format(self.parking_lot.name)
    return prefix + filename


class ParkingLotImage(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    image = models.ImageField(upload_to=get_image_path)
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_image'
        verbose_name = "駐車場画像"
        verbose_name_plural = "駐車場画像一覧"


class ParkingLotDoc(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    document = models.FileField(upload_to=get_doc_path)
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_doc'
        verbose_name = "駐車場書類"
        verbose_name_plural = "駐車場書類一式"


class ParkingPosition(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    name = models.CharField(max_length=30, verbose_name="車室名称")
    # 賃料
    price_recruitment = models.IntegerField(default=0, verbose_name="募集賃料（税込）")
    price_recruitment_no_tax = models.IntegerField(default=0, verbose_name="募集賃料（税抜）")
    price_homepage = models.IntegerField(default=0, verbose_name="ホームページ価格（税込）")
    price_homepage_no_tax = models.IntegerField(default=0, verbose_name="ホームページ価格（税別）")
    price_handbill = models.IntegerField(default=0, verbose_name="チラシ価格（税込）")
    price_handbill_no_tax = models.IntegerField(default=0, verbose_name="チラシ価格（税別）")
    # サイズ
    length = models.IntegerField(blank=True, null=True, verbose_name="全長")
    width = models.IntegerField(blank=True, null=True, verbose_name="全幅")
    height = models.IntegerField(blank=True, null=True, verbose_name="全高")
    weight = models.IntegerField(blank=True, null=True, verbose_name="重量")
    tyre_width = models.IntegerField(blank=True, null=True, verbose_name="ﾒｰｶｰのタイヤ幅")
    tyre_width_ap = models.IntegerField(blank=True, null=True, verbose_name="AP計測のタイヤ幅")
    min_height = models.IntegerField(blank=True, null=True, verbose_name="ﾒｰｶｰの地上最低高")
    min_height_ap = models.IntegerField(blank=True, null=True, verbose_name="AP計測の地上最低高")
    f_value = models.IntegerField(blank=True, null=True, verbose_name="F値")
    r_value = models.IntegerField(blank=True, null=True, verbose_name="R値")
    time_limit = models.ForeignKey(ParkingTimeLimit, blank=True, null=True, verbose_name="時間制限")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_position'
        unique_together = ('parking_lot', 'name')
        ordering = ['name']
        verbose_name = "車室"
        verbose_name_plural = "車室一覧"

    def __unicode__(self):
        return self.name

    def contracts(self, date=None):
        if not date:
            date = datetime.date.today()
        contracts = self.contract_set.filter(start_date__lte=date, end_date__gte=date)
        return contracts

    def temp_contracts(self):
        """手続き中の契約を取得する。

        :return:
        """
        queryset = self.tempcontract_set.filter(start_date__gte=datetime.date.today())
        return queryset
