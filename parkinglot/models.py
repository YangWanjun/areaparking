# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime

from django.db import models
from django.db.models import Q

from master.models import ParkingTimeLimit
from utils.django_base import BaseModel


# Create your models here.
class ParkingLot(BaseModel):
    code = models.IntegerField(primary_key=True, verbose_name="物件番号")
    name = 
    lng = models.FloatField(blank=True, null=True, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, verbose_name="緯度")
    is_existed_contractor_allowed = models.BooleanField(default=False, verbose_name="既契約者")
    is_new_contractor_allowed = models.BooleanField(default=False, verbose_name="新テナント")
    free_end_date = models.DateField(blank=True, null=True, verbose_name="フリーレント終了日")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        managed = False
        db_table = 'ap_parking_lot'
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __str__(self):
        return str(self.buken)

    def address(self):
        if self.buken:
            return "{}{}{}{}{}".format(
                self.buken.add_ken, self.buken.add_si, self.buken.add_cyo or '',
                self.buken.add_banti or '', self.buken.add_etc or ''
            )
        else:
            return None


def get_image_path(self, filename):
    prefix = 'images/'
    name = '{}_{}'.format(self.parking_lot.name, datetime.datetime.now().strftime('%y%m%d%H%M%S%f'))
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_doc_path(self, filename):
    prefix = 'docs/{}/'.format(self.parking_lot.name)
    return prefix + filename


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
    price_recruitment = models.IntegerField(blank=True, null=True, verbose_name="募集賃料（税込）")
    price_recruitment_no_tax = models.IntegerField(blank=True, null=True, verbose_name="募集賃料（税抜）")
    price_homepage = models.IntegerField(blank=True, null=True, verbose_name="ホームページ価格（税込）")
    price_homepage_no_tax = models.IntegerField(blank=True, null=True, verbose_name="ホームページ価格（税別）")
    price_handbill = models.IntegerField(blank=True, null=True, verbose_name="チラシ価格（税込）")
    price_handbill_no_tax = models.IntegerField(blank=True, null=True, verbose_name="チラシ価格（税別）")
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

    def __str__(self):
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
        queryset = self.tempcontract_set.filter(Q(start_date__gte=datetime.date.today()) | Q(start_date__isnull=True))
        return queryset


class VParkingLotSummary(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="名称")
    lng = models.FloatField(blank=True, null=True, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, verbose_name="緯度")
    is_existed_contractor_allowed = models.BooleanField(default=False, verbose_name="既契約者")
    is_new_contractor_allowed = models.BooleanField(default=False, verbose_name="新テナント")
    free_end_date = models.DateField(blank=True, null=True, verbose_name="フリーレント終了日")
    position_count = models.IntegerField(verbose_name="車室数")
    contract_count = models.IntegerField(verbose_name="契約数")

    class Meta:
        managed = False
        db_table = 'v_parkinglot_summary'
        verbose_name = "駐車場概要"
        verbose_name_plural = "駐車場概要一覧"

    def __str__(self):
        return self.name
