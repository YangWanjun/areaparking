# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from parkinglot.models import ParkingLot, ParkingPosition


# Create your models here.
class WhiteBoard(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    parking_lot = models.ForeignKey(ParkingLot, blank=True, null=True, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, blank=True, null=True, verbose_name="車室")
    bk_no = models.IntegerField(verbose_name="物件番号")
    seq_no = models.SmallIntegerField(db_column='naibu_no', verbose_name="内部番号")
    position_name = models.CharField(max_length=30, verbose_name="車室名称")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="場所")
    is_existed_contractor_allowed = models.BooleanField(default=False, verbose_name="既契約者")
    is_new_contractor_allowed = models.BooleanField(default=False, verbose_name="新テナント")
    free_end_date = models.DateField(blank=True, null=True, verbose_name="フリーレント終了日")
    lot_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="駐車場備考")
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
    time_limit_id = models.IntegerField(blank=True, null=True, verbose_name="時間制限")
    position_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        managed = False
        db_table = 'v_whiteboard'
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __unicode__(self):
        return str(self.bk_no)
