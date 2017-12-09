# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from parkinglot.models import ParkingLot, ParkingPosition, ParkingLotType, ParkingTimeLimit
from employee.models import Member
from utils import constants


# Create your models here.
class WhiteBoard(models.Model):
    parking_code = models.IntegerField(verbose_name="物件番号")
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    parking_lot_name = models.CharField(max_length=100, verbose_name="駐車場名称")
    staff = models.ForeignKey(Member, blank=True, null=True, verbose_name="担当者")
    category = models.ForeignKey(ParkingLotType, verbose_name="駐車場分類")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="場所")
    lng = models.FloatField(blank=True, null=True, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, verbose_name="緯度")
    position_count = models.IntegerField(default=0, verbose_name="管理台数")
    waiting_count = models.IntegerField(default=0, verbose_name="順番待ち")
    is_existed_contractor_allowed = models.BooleanField(default=False, verbose_name="既契約者")
    is_new_contractor_allowed = models.BooleanField(default=False, verbose_name="新テナント")
    free_end_date = models.DateField(blank=True, null=True, verbose_name="フリーレント終了日")
    parking_time_limit = models.ForeignKey(ParkingTimeLimit, blank=True, null=True, verbose_name="時間制限")
    # 車室情報
    parking_position = models.ForeignKey(ParkingPosition, blank=True, null=True, verbose_name="車室")
    contract_status = models.CharField(max_length=2, choices=constants.CHOICE_CONTRACT_STATUS, verbose_name="空き")
    contract_end_date = models.DateField(blank=True, null=True, verbose_name="契約終了日")
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
    position_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        managed = False
        db_table = 'v_whiteboard'
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __str__(self):
        return self.parking_lot_name


# class Waiting(BaseModel):
#     parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
#     tanto_no = models.IntegerField(blank=True, null=True, verbose_name="担当者")
#     name = models.CharField(max_length=50, verbose_name="氏名")
#     tel1 = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号１")
#     tel2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号２")
#     address1 = models.CharField(max_length=50, blank=True, null=True, verbose_name="住所１")
#     address2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="住所２")
#     email = models.CharField(max_length=50, blank=True, null=True, verbose_name="メール")
#     contractor_id = models.IntegerField(blank=True, null=True, verbose_name="契約者")
#     # 車情報
#     car_maker = models.CharField(max_length=30, blank=True, null=True, verbose_name="メーカー")
#     car_model = models.CharField(max_length=50, blank=True, null=True, verbose_name="車種")
#     length = models.IntegerField(blank=True, null=True, verbose_name="全長")
#     width = models.IntegerField(blank=True, null=True, verbose_name="全幅")
#     height = models.IntegerField(blank=True, null=True, verbose_name="全高")
#     weight = models.IntegerField(blank=True, null=True, verbose_name="重量")
#     media = models.ForeignKey(TransmissionRoute, blank=True, null=True, verbose_name="媒体")
#     price_handbill = models.CharField(max_length=30, blank=True, null=True, verbose_name="いくらのチラシか")
#     comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="AP備考・特記")
#
#     class Meta:
#         db_table = 'ap_waiting_list'
#         verbose_name = "順番待ち"
#         verbose_name_plural = "順番待ちリスト"
#
#     def __str__(self):
#         return "%s-%s" % (str(self.parking_lot), self.name)
#
#     @property
#     def contractor(self):
#         if self.contractor_id:
#             try:
#                 return KysMst.objects.get(pk=self.contractor_id)
#             except ObjectDoesNotExist:
#                 return None
#         else:
#             return None
#
#
# class WaitingContact(BaseModel):
#     waiting = models.ForeignKey(Waiting, verbose_name="順番待ち")
#     contact_date = models.DateField(verbose_name="連絡日")
#     comment = models.CharField(max_length=255, verbose_name="備考・特記")
#
#     class Meta:
#         db_table = 'ap_waiting_contact'
#         verbose_name = "連絡履歴"
#         verbose_name_plural = "連絡リスト"
#
#     def __str__(self):
#         return self.comment
