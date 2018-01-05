# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from parkinglot.models import ParkingPosition, ParkingLotType
from employee.models import Member
from utils import constants
from utils.django_base import BaseViewModel, BaseModel


# Create your models here.
class WhiteBoard(BaseViewModel):
    code = models.IntegerField(primary_key=True, verbose_name="コード")
    name = models.CharField(max_length=100, verbose_name="駐車場名称")
    category = models.ForeignKey(ParkingLotType, on_delete=models.DO_NOTHING, verbose_name="分類")
    staff = models.ForeignKey(Member, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="担当者")
    address = models.CharField(max_length=255, blank=True, null=True, editable=False, verbose_name="所在地")
    lng = models.FloatField(blank=True, null=True, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, verbose_name="緯度")
    position_count = models.IntegerField(default=0, editable=False, verbose_name="車室数")
    contract_count = models.IntegerField(default=0, editable=False, verbose_name="契約数")
    temp_contract_count = models.IntegerField(default=0, editable=False, verbose_name="手続中")
    waiting_count = models.IntegerField(default=0, editable=False, verbose_name="待ち数")
    is_existed_contractor_allowed = models.BooleanField(default=False, verbose_name="既契約者")
    is_new_contractor_allowed = models.BooleanField(default=False, verbose_name="新テナント")
    free_end_date = models.DateField(blank=True, null=True, verbose_name="フリーレント終了日")

    class Meta:
        managed = False
        db_table = 'v_whiteboard'
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __str__(self):
        return self.name

    def is_empty(self):
        if self.position_count == self.contract_count:
            # 空無
            return '03'
        elif self.position_count == (self.contract_count + self.temp_contract_count):
            # 手続中
            return '02'
        else:
            # 空き
            return '01'

    def operation(self):
        return ''

    is_empty.short_description = '空き'
    operation.short_description = ''


class WhiteBoardPosition(BaseViewModel):
    whiteboard = models.ForeignKey(WhiteBoard, on_delete=models.DO_NOTHING, verbose_name="ホワイトボード")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.DO_NOTHING, verbose_name="車室")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="所在地")
    position_status = models.CharField(max_length=2, choices=constants.CHOICE_PARKING_STATUS, verbose_name="空き")
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
        db_table = 'v_whiteboard_position'
        verbose_name = "車室"
        verbose_name_plural = "車室一覧"

    def __str__(self):
        return str(self.parking_position)


class Inquiry(BaseModel):
    user_name = models.CharField(blank=True, null=True, max_length=15, verbose_name="名前")
    gender = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_GENDER, verbose_name="性別")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    parking_lot_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="希望する駐車場コード")
    parking_lot_name = models.CharField(blank=True, null=True, max_length=100, verbose_name="希望する駐車場名称")
    area_code = models.CharField(blank=True, null=True, max_length=20, verbose_name="希望するエリアコード")
    area_name = models.CharField(blank=True, null=True, max_length=50, verbose_name="希望するエリア名称")
    transmission_routes = models.CharField(blank=True, null=True, max_length=20, verbose_name="媒体",
                                           validators=[validate_comma_separated_integer_list],
                                           help_text='どのようにして､この駐車場を知りましたか？')
    transmission_handbill_price = models.IntegerField(blank=True, null=True, verbose_name="チラシ価格")
    transmission_other_route = models.CharField(blank=True, null=True, max_length=50, verbose_name="その他の媒体")
    car_maker = models.CharField(max_length=50, blank=True, null=True, verbose_name="車メーカー")
    car_model = models.CharField(max_length=100, blank=True, null=True, verbose_name="車種")
    car_length = models.IntegerField(blank=True, null=True, verbose_name="全長")
    car_width = models.IntegerField(blank=True, null=True, verbose_name="全幅")
    car_height = models.IntegerField(blank=True, null=True, verbose_name="全高")
    car_weight = models.IntegerField(blank=True, null=True, verbose_name="重量")
    car_min_height = models.IntegerField(blank=True, null=True, verbose_name="地上最低高")
    car_f_value = models.IntegerField(blank=True, null=True, verbose_name="F値")
    car_r_value = models.IntegerField(blank=True, null=True, verbose_name="R値")
    comment = models.CharField(blank=True, null=True, max_length=255, verbose_name="備考")

    class Meta:
        db_table = 'ap_inquiry'
        verbose_name = "ユーザー問い合わせ"
        verbose_name_plural = "ユーザー問い合わせ"

    def __str__(self):
        return self.user_name

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
