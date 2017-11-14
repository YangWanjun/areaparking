# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from master.models import TransmissionRoute
from parkinglot.models import ParkingLot, ParkingPosition
from revolution.models import KysMst

from utils.django_base import BaseModel


# Create your models here.
class WhiteBoard(models.Model):
    id = models.CharField(max_length=18, primary_key=True, editable=False)
    parking_lot = models.ForeignKey(ParkingLot, blank=True, null=True, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, blank=True, null=True, verbose_name="車室")
    bk_no = models.IntegerField(verbose_name="物件番号")
    bk_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="駐車場名称")
    position_count = models.IntegerField(default=0, verbose_name="管理台数")
    waiting_count = models.IntegerField(default=0, verbose_name="順番待ち")
    position_name = models.CharField(max_length=30, verbose_name="車室名称")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="場所")
    contract_status = models.CharField(max_length=10, blank=True, null=True, verbose_name="空き")
    tanto_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="担当者名前")
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
        return self.bk_name if self.bk_name else str(self.bk_no)


class Waiting(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    tanto_no = models.IntegerField(blank=True, null=True, verbose_name="担当者")
    name = models.CharField(max_length=50, verbose_name="氏名")
    tel1 = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号１")
    tel2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号２")
    address1 = models.CharField(max_length=50, blank=True, null=True, verbose_name="住所１")
    address2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="住所２")
    email = models.CharField(max_length=50, blank=True, null=True, verbose_name="メール")
    contractor_id = models.IntegerField(blank=True, null=True, verbose_name="契約者")
    # 車情報
    car_maker = models.CharField(max_length=30, blank=True, null=True, verbose_name="メーカー")
    car_model = models.CharField(max_length=50, blank=True, null=True, verbose_name="車種")
    length = models.IntegerField(blank=True, null=True, verbose_name="全長")
    width = models.IntegerField(blank=True, null=True, verbose_name="全幅")
    height = models.IntegerField(blank=True, null=True, verbose_name="全高")
    weight = models.IntegerField(blank=True, null=True, verbose_name="重量")
    media = models.ForeignKey(TransmissionRoute, blank=True, null=True, verbose_name="媒体")
    price_handbill = models.CharField(max_length=30, blank=True, null=True, verbose_name="いくらのチラシか")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="AP備考・特記")

    class Meta:
        db_table = 'ap_waiting_list'
        verbose_name = "順番待ち"
        verbose_name_plural = "順番待ちリスト"

    def __unicode__(self):
        return "%s-%s" % (unicode(self.parking_lot), self.name)

    @property
    def contractor(self):
        if self.contractor_id:
            try:
                return KysMst.objects.get(pk=self.contractor_id)
            except ObjectDoesNotExist:
                return None
        else:
            return None


class WaitingContact(BaseModel):
    waiting = models.ForeignKey(Waiting, verbose_name="順番待ち")
    contact_date = models.DateField(verbose_name="連絡日")
    comment = models.CharField(max_length=255, verbose_name="備考・特記")

    class Meta:
        db_table = 'ap_waiting_contact'
        verbose_name = "連絡履歴"
        verbose_name_plural = "連絡リスト"

    def __unicode__(self):
        return self.comment
