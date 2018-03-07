import os
import datetime
import math
from collections import defaultdict

from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.shortcuts import reverse
from django.utils.functional import cached_property

from employee.models import Member
from master.models import Config
from utils.django_base import BaseModel
from utils import constants, common


# Create your models here.
class ParkingLotType(BaseModel):
    code = models.SmallIntegerField(primary_key=True, verbose_name="分類コード",
                                    validators=(RegexValidator(regex=r'^\d{1,4}$'),))
    name = models.CharField(max_length=30, verbose_name="名称")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_type'
        ordering = ['code']
        verbose_name = "駐車場分類"
        verbose_name_plural = "駐車場分類一覧"

    def __str__(self):
        return self.name


# class LeaseManagementCompany(BaseModel):
#     name = models.CharField(max_length=100, verbose_name="会社名")
#     department = models.CharField(max_length=30, blank=True, null=True, verbose_name="部署")
#     position = models.CharField(max_length=30, blank=True, null=True, verbose_name="役職")
#     staff = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者")
#     address = models.CharField(max_length=100, blank=True, null=True, verbose_name="所在地")
#     tel = models.CharField(max_length=15, blank=True, null=True, verbose_name="電話番号",
#                            validators=(RegexValidator(regex=constants.REG_TEL),))
#     fax = models.CharField(max_length=15, blank=True, null=True, verbose_name="FAX番号",
#                            validators=(RegexValidator(regex=constants.REG_TEL),))
#     phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="FAX番号",
#                              validators=(RegexValidator(regex=constants.REG_TEL),))
#     email = models.EmailField(blank=True, null=True, verbose_name="メール")
#     comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
#
#     class Meta:
#         db_table = 'ap_lease_management_company'
#         ordering = ['name']
#         verbose_name = "賃貸管理会社"
#         verbose_name_plural = "賃貸管理会社一覧"
#
#     def __str__(self):
#         return self.name
#
#
# class BuildingManagementCompany(BaseModel):
#     name = models.CharField(max_length=100, verbose_name="会社名")
#     department = models.CharField(max_length=30, blank=True, null=True, verbose_name="部署")
#     position = models.CharField(max_length=30, blank=True, null=True, verbose_name="役職")
#     staff = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者")
#     address = models.CharField(max_length=100, blank=True, null=True, verbose_name="所在地")
#     tel = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号",
#                            validators=(RegexValidator(regex=constants.REG_TEL),))
#     fax = models.CharField(max_length=20, blank=True, null=True, verbose_name="FAX番号",
#                            validators=(RegexValidator(regex=constants.REG_TEL),))
#     phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="FAX番号",
#                              validators=(RegexValidator(regex=constants.REG_TEL),))
#     email = models.EmailField(blank=True, null=True, verbose_name="メール")
#     comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
#
#     class Meta:
#         db_table = 'ap_building_management_company'
#         ordering = ['name']
#         verbose_name = "建物管理会社"
#         verbose_name_plural = "建物管理会社一覧"
#
#     def __str__(self):
#         return self.name


class ManagementCompany(BaseModel):
    name = models.CharField(max_length=100, verbose_name="会社名")
    # department = models.CharField(max_length=30, blank=True, null=True, verbose_name="部署")
    # position = models.CharField(max_length=30, blank=True, null=True, verbose_name="役職")
    # staff = models.CharField(max_length=30, blank=True, null=True, verbose_name="担当者")
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name="所在地")
    tel = models.CharField(max_length=15, blank=True, null=True, verbose_name="電話番号",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    fax = models.CharField(max_length=15, blank=True, null=True, verbose_name="FAX番号",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="携帯番号",
                             validators=(RegexValidator(regex=constants.REG_TEL),))
    email = models.EmailField(blank=True, null=True, verbose_name="メール")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_management_company'
        ordering = ['name']
        verbose_name = "管理会社"
        verbose_name_plural = "管理会社一覧"

    def __str__(self):
        return self.name


class ManagementCompanyStaff(BaseModel):
    company = models.ForeignKey(ManagementCompany, related_name='staff_set', verbose_name="管理会社")
    name = models.CharField(max_length=30, verbose_name="名前")
    department = models.CharField(max_length=30, blank=True, null=True, verbose_name="部署")
    position = models.CharField(max_length=30, blank=True, null=True, verbose_name="役職")
    tel = models.CharField(max_length=15, blank=True, null=True, verbose_name="電話番号",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    fax = models.CharField(max_length=15, blank=True, null=True, verbose_name="FAX番号",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="携帯番号",
                             validators=(RegexValidator(regex=constants.REG_TEL),))
    email = models.EmailField(blank=True, null=True, verbose_name="メール")

    class Meta:
        db_table = 'ap_management_company_staff'
        ordering = ['name']
        verbose_name = "管理会社担当者"
        verbose_name_plural = "管理会社担当者一覧"

    def __str__(self):
        return self.name


class TryPuttingOperator(BaseModel):
    name = models.CharField(max_length=30, verbose_name="名称")

    class Meta:
        db_table = 'ap_try_putting'
        ordering = ['name']
        verbose_name = "試し入れ"
        verbose_name_plural = "試し入れ一覧"

    def __str__(self):
        return self.name


class ParkingLot(BaseModel):
    # 物件基本情報
    code = models.IntegerField(primary_key=True, verbose_name="物件番号")
    name = models.CharField(max_length=100, verbose_name="駐車場名称")
    kana = models.CharField(max_length=100, blank=True, null=True, verbose_name="駐車場カナ")
    category = models.ForeignKey(ParkingLotType, verbose_name="駐車場分類")
    post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name="郵便番号",
                                 validators=(RegexValidator(regex=constants.REG_POST_CODE),))
    pref_code = models.CharField(max_length=2, blank=True, null=True, editable=False, verbose_name="都道府県コード")
    pref_name = models.CharField(max_length=15, verbose_name="都道府県名称")
    city_code = models.CharField(max_length=5, blank=True, null=True, editable=False, verbose_name="市区町村コード")
    city_name = models.CharField(max_length=15, verbose_name="市区町村名称")
    town_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="町域名称")
    aza_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="丁番地")
    other_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="その他")
    lng = models.FloatField(blank=True, null=True, editable=False, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, editable=False, verbose_name="緯度")
    point = models.PointField(blank=True, null=True, editable=False, verbose_name="座標")
    # 交通情報
    nearest_station_line1 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅① 沿線名")
    nearest_station_name1 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅① 駅名")
    nearest_station_walk1 = models.SmallIntegerField(blank=True, null=True, verbose_name="最寄駅① 徒歩（分）")
    nearest_station_line2 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅② 沿線名")
    nearest_station_name2 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅② 駅名")
    nearest_station_walk2 = models.SmallIntegerField(blank=True, null=True, verbose_name="最寄駅② 徒歩（分）")
    # 貸主・所有者・管理会社
    owner = models.CharField(max_length=50, blank=True, null=True, verbose_name="所有者")
    lender = models.CharField(max_length=50, blank=True, null=True, verbose_name="貸主")
    lease_management_company = models.ForeignKey(
        ManagementCompany, blank=True, null=True, related_name='lease_parking_lot_set', verbose_name="賃貸管理会社"
    )
    lease_management_company_staff = models.ManyToManyField(
        ManagementCompanyStaff, blank=True,
        related_name='lease_staff_parking_lot_set', verbose_name="賃貸管理会社担当者"
    )
    building_management_company = models.ForeignKey(
        ManagementCompany, blank=True, null=True, related_name='building_parking_lot_set', verbose_name="建物管理会社"
    )
    building_management_company_staff = models.ManyToManyField(
        ManagementCompanyStaff, blank=True,
        related_name='building_staff_parking_lot_set', verbose_name="建物管理会社担当者"
    )
    subscription_list_send_type = models.CharField(
        max_length=2, blank=True, null=True, default='01', choices=constants.CHOICE_SUBSCRIPTION_LIST_SEND_TYPE,
        verbose_name="申込者送付先"
    )
    # 駐車場概要
    is_condominium = models.BooleanField(default=False, verbose_name="分譲マンション")
    car_count = models.IntegerField(default=0, verbose_name="駐車場総台数")
    entering_method = models.CharField(max_length=30, blank=True, null=True, verbose_name="入出庫方法")
    has_turntable = models.BooleanField(default=False, verbose_name="ターンテーブルの有無")
    has_palette = models.BooleanField(default=False, verbose_name="専用パレット")
    admin_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="管理員氏名")
    admin_kana = models.CharField(max_length=30, blank=True, null=True, verbose_name="管理員カナ")
    admin_tel = models.CharField(max_length=15, blank=True, null=True, verbose_name="管理員電話番号",
                                 validators=(RegexValidator(regex=constants.REG_TEL),))
    admin_time = models.CharField(max_length=30, blank=True, null=True, verbose_name="管理員勤務時間帯")
    # 物件管理情報
    management_type = models.CharField(max_length=2, default='02', choices=constants.CHOICE_MANAGEMENT_TYPE,
                                       verbose_name="管理形態")
    start_date = models.DateField(blank=True, null=True, verbose_name="契約開始日")
    end_date = models.DateField(blank=True, null=True, default=constants.END_DATE, verbose_name="契約終了日")
    free_end_date = models.DateField(blank=True, null=True, verbose_name="フリーレント終了日")
    lease_count = models.SmallIntegerField(default=0, verbose_name="サブリース台数")
    has_tenant_sign = models.BooleanField(default=False, verbose_name="ＡＰ募集看板の設置")
    has_call_center = models.BooleanField(default=False, verbose_name="コールセンターの設置")
    try_putting_operator = models.ForeignKey(TryPuttingOperator, blank=True, null=True, verbose_name="試入れの対応者")
    is_existed_contractor_allowed = models.BooleanField(default=False, verbose_name="既契約者")
    is_new_contractor_allowed = models.BooleanField(default=False, verbose_name="新テナント")
    required_insurance = models.BooleanField(default=True, verbose_name="任意保険回収必須")
    # その他の情報
    default_contract_months = models.SmallIntegerField(default=12, verbose_name="契約期間初期値",
                                                       help_text='月単位です、１年の場合は１２を入力してください。')
    staff = models.ForeignKey(Member, blank=True, null=True, verbose_name="担当者")
    staff_start_date = models.DateField(blank=True, null=True, verbose_name="担当開始日")
    time_limit_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="利用時間帯について")
    transit_pass_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="通行許可証について")

    class Meta:
        db_table = 'ap_parking_lot'
        ordering = ['post_code', 'city_code', 'town_name', 'aza_name', 'other_name']
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __str__(self):
        return self.name

    @cached_property
    def address(self):
        return "{}{}{}{}{}".format(
            self.pref_name, self.city_name, self.town_name or '', self.aza_name or '', self.other_name or ''
        )

    address.short_description = '所在地'

    @cached_property
    def waiting_count(self):
        """この駐車場の空き待ち数

        :return:
        """
        return self.waitingparkinglot_set.count()

    def get_suitable_positions(self, length, width, height, weight):
        """指定した車のサイズによって、該当する車室リストを取得する。

        :param length:
        :param width:
        :param height:
        :param weight:
        :return:
        """
        if not length or not width or not height or not weight:
            return [None]
        positions = ParkingPosition.objects.public_filter(parking_lot=self)
        suitable_list = []
        adjust_length = Config.get_car_length_adjust()
        adjust_width = Config.get_car_width_adjust()
        adjust_height = Config.get_car_height_adjust()
        adjust_weight = Config.get_car_weight_adjust()
        for position in positions:
            is_suitable = True
            length_suitable = True
            width_suitable = True
            height_suitable = True
            weight_suitable = True
            if position.length + adjust_length < length:
                is_suitable = length_suitable = False
            if position.width + adjust_width < width:
                is_suitable = width_suitable = False
            if position.height + adjust_height < height:
                is_suitable = height_suitable = False
            if position.weight + adjust_weight < weight:
                is_suitable = weight_suitable = False

            suitable_list.append({
                'is_suitable': is_suitable,
                'position': position,
                'length_suitable': length_suitable,
                'width_suitable': width_suitable,
                'height_suitable': height_suitable,
                'weight_suitable': weight_suitable,
                'adjust_length': adjust_length,
                'adjust_width': adjust_width,
                'adjust_height': adjust_height,
                'adjust_weight': adjust_weight,
            })
        return suitable_list

    def get_size_grouped_position(self):
        """駐車可能サイズを取得する。

        :return:
        """
        queryset = ParkingPosition.objects.public_filter(parking_lot=self).values(
            'length', 'width', 'height', 'weight', 'min_height'
        ).annotate(position_count=models.Count('length'))
        return queryset

    def get_lacking_keys(self):
        """鍵の足りない本数を取得する。

        :return:
        """
        # 駐車場の残り鍵警告比率
        alert_percent = Config.get_parking_lot_key_alert_percent()
        # 予備鍵本数
        reserve_keys = dict()
        reserve_queryset = ParkingLotKey.objects.public_filter(parking_lot=self).exclude(category='04').values(
            'category', 'key_count'
        )
        for parking_lot_key in reserve_queryset:
            reserve_keys[parking_lot_key.get('category')] = parking_lot_key.get('key_count')
        # 各車室の鍵数
        position_queryset = ParkingPosition.objects.public_filter(parking_lot=self)
        keys_with_position = defaultdict(lambda: 0)
        position_key_queryset = ParkingPositionKey.objects.public_filter(
                parking_position__in=position_queryset,
        ).exclude(category='04')
        for position_key in position_key_queryset:
            keys_with_position[position_key.category] += position_key.key_count
        # 足りない分の鍵本数
        lacking_keys = dict()
        for category, count in keys_with_position.items():
            required_count = math.ceil(count * alert_percent)
            reserve_count = reserve_keys.get(category, 0)
            if required_count > reserve_count:
                lacking_keys[category] = required_count - reserve_count
        return lacking_keys.items()

    def get_absolute_url(self):
        return reverse('whiteboard:whiteboard_detail', args=(self.pk,))


class ParkingLotKey(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    category = models.CharField(max_length=2, choices=constants.CHOICE_KEY_CATEGORY, verbose_name="種類")
    key_count = models.SmallIntegerField(default=1, verbose_name="本数")
    comment = models.CharField(blank=True, null=True, max_length=250, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_key'
        unique_together = ('parking_lot', 'category')
        ordering = ['parking_lot', 'category']
        verbose_name = "駐車場予備鍵"
        verbose_name_plural = "駐車場予備鍵一覧"

    def __str__(self):
        return self.category


class ParkingLotStaffHistory(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    member = models.ForeignKey(Member, verbose_name="担当者")
    start_date = models.DateField(verbose_name="開始日")
    end_date = models.DateField(verbose_name="終了日")

    class Meta:
        db_table = 'ap_parking_lot_staff_history'
        ordering = ['parking_lot', 'member']
        verbose_name = "駐車場担当者履歴"
        verbose_name_plural = "駐車場担当者履歴一覧"

    def __str__(self):
        return "{} - {}".format(str(self.parking_lot), str(self.member))


class ParkingLotComment(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    comment = models.CharField(max_length=255, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_comment'
        verbose_name = "注意事項・備考"
        verbose_name_plural = "注意事項・備考一覧"

    def __str__(self):
        return self.comment


class ParkingLotDoc(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    path = models.FileField(upload_to=common.get_parking_lot_doc_path)
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_doc'
        verbose_name = "駐車場書類"
        verbose_name_plural = "駐車場書類一式"

    def __str__(self):
        return os.path.basename(str(self.path))


class ParkingLotImage(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    path = models.ImageField(upload_to=common.get_parking_lot_image_path)
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_lot_image'
        verbose_name = "駐車場画像"
        verbose_name_plural = "駐車場画像一覧"

    def __str__(self):
        return os.path.basename(str(self.path))


class ParkingPosition(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    name = models.CharField(max_length=30,
                            validators=(
                                RegexValidator(regex=constants.REG_MULTI_POSITIONS),
                            ),
                            verbose_name="車室番号",
                            help_text='新規追加時、連番で追加したい場合：1-10（車室番号は１から１０まで追加される）；'
                                      '連番出ない場合：1,3,5,7（車室番号は１、３、５、７が追加される）。')
    category = models.ForeignKey(ParkingLotType, verbose_name="駐車場分類")
    # 賃料
    price_recruitment = models.IntegerField(blank=True, null=True, verbose_name="募集賃料（税込）")
    price_recruitment_no_tax = models.IntegerField(blank=True, null=True, verbose_name="募集賃料（税別）")
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
    # 貸止め
    is_lock = models.BooleanField(default=False, verbose_name="貸止め")
    lock_content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    lock_object_id = models.PositiveIntegerField(blank=True, null=True)
    lock_content_object = GenericForeignKey('lock_content_type', 'lock_object_id')
    lock_reason = models.CharField(max_length=100, blank=True, null=True, verbose_name="貸止め理由")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_position'
        unique_together = ('parking_lot', 'name')
        ordering = ['name']
        verbose_name = "車室"
        verbose_name_plural = "車室一覧"

    def __str__(self):
        return str(self.name)

    def get_current_contract(self):
        today = datetime.date.today()
        queryset = self.contract_set.filter(start_date__lte=today, end_date__gte=today)
        return queryset.first()

    @cached_property
    def status(self):
        if self.get_current_contract():
            # 空き無
            return '03'
        else:
            # TODO:貸止め等他のステータス
            # 空き
            return '01'

    def get_absolute_url(self):
        return reverse('whiteboard:whiteboard_position_detail', args=(self.pk,))


class ParkingPositionKey(BaseModel):
    parking_position = models.ForeignKey(ParkingPosition, verbose_name="車室")
    category = models.CharField(max_length=2, choices=constants.CHOICE_KEY_CATEGORY, verbose_name="種類")
    key_count = models.SmallIntegerField(default=1, verbose_name="本数")
    password = models.CharField(blank=True, null=True, max_length=20, verbose_name="パスワード")
    comment = models.CharField(blank=True, null=True, max_length=250, verbose_name="備考")

    class Meta:
        db_table = 'ap_parking_position_key'
        unique_together = ('parking_position', 'category')
        ordering = ['parking_position', 'category']
        verbose_name = "車室鍵情報"
        verbose_name_plural = "車室鍵情報一覧"

    def __str__(self):
        return self.category
