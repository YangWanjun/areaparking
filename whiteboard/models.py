from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from django.db import models

from address.models import City, Aza
from contract.models import Contractor, ContactHistory, Contract
from parkinglot.models import ParkingPosition, ParkingLotType, ParkingLot, TryPuttingOperator
from employee.models import Member
from master.models import TransmissionRoute
from utils import constants, errors
from utils.django_base import BaseViewModel, BaseModel


# Create your models here.
class WhiteBoard(BaseViewModel):
    code = models.CharField(max_length=10, primary_key=True, verbose_name="コード")
    name = models.CharField(max_length=100, verbose_name="駐車場名称")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.DO_NOTHING, verbose_name="駐車場")
    category = models.ForeignKey(ParkingLotType, on_delete=models.DO_NOTHING, verbose_name="分類")
    staff = models.ForeignKey(Member, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="担当者")
    address = models.CharField(max_length=255, blank=True, null=True, editable=False, verbose_name="所在地")
    lng = models.FloatField(blank=True, null=True, verbose_name="経度")
    lat = models.FloatField(blank=True, null=True, verbose_name="緯度")
    position_count = models.IntegerField(default=0, editable=False, verbose_name="車室数")
    contract_count = models.IntegerField(default=0, editable=False, verbose_name="契約数")
    temp_contract_count = models.IntegerField(default=0, editable=False, verbose_name="手続中")
    lock_count = models.IntegerField(default=0, editable=False, verbose_name="貸止数")
    waiting_count = models.IntegerField(default=0, editable=False, verbose_name="待ち数")
    is_existed_contractor_allowed = models.BooleanField(default=False, verbose_name="既契約者")
    is_new_contractor_allowed = models.BooleanField(default=False, verbose_name="新テナント")
    free_end_date = models.DateField(blank=True, null=True, verbose_name="フリーレント終了日")
    required_insurance = models.BooleanField(default=True, verbose_name="保険回収必須")
    has_time_limit = models.BooleanField(verbose_name="時間制限")
    is_required_try_putting = models.BooleanField(default=False, verbose_name="試し入れ必須")
    try_putting_operator = models.ForeignKey(TryPuttingOperator, blank=True, null=True, verbose_name="試入れの対応者")
    time_limit_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="利用時間帯について")
    transit_pass_comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="通行許可証について")
    # 交通情報
    nearest_station_line1 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅① 沿線名")
    nearest_station_name1 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅① 駅名")
    nearest_station_walk1 = models.SmallIntegerField(blank=True, null=True, verbose_name="最寄駅① 徒歩（分）")
    nearest_station_line2 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅② 沿線名")
    nearest_station_name2 = models.CharField(max_length=30, blank=True, null=True, verbose_name="最寄駅② 駅名")
    nearest_station_walk2 = models.SmallIntegerField(blank=True, null=True, verbose_name="最寄駅② 徒歩（分）")

    class Meta:
        managed = False
        db_table = 'v_whiteboard'
        verbose_name = "駐車場"
        verbose_name_plural = "駐車場一覧"

    def __str__(self):
        return str(self.parking_lot)

    def is_empty(self):
        if self.position_count == self.contract_count:
            # 空無
            return '03'
        elif self.position_count == (self.contract_count + self.temp_contract_count):
            # 手続中
            return '02'
        elif self.position_count == (self.contract_count + self.temp_contract_count + self.lock_count):
            return '05'
        else:
            # 空き
            return '01'

    def operation(self):
        return self.code

    is_empty.short_description = '空き'
    operation.short_description = ''


class WhiteBoardPosition(BaseViewModel):
    whiteboard = models.ForeignKey(WhiteBoard, on_delete=models.DO_NOTHING, verbose_name="ホワイトボード")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.DO_NOTHING, verbose_name="車室")
    name = models.CharField(max_length=30, verbose_name="車室番号")
    category = models.ForeignKey(ParkingLotType, on_delete=models.DO_NOTHING, verbose_name="分類")
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
    is_lock = models.BooleanField(default=False, verbose_name="貸止め")
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
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    is_tenant = models.BooleanField(default=False, verbose_name="入居者")
    target_parking_lot_code = models.IntegerField(blank=True, null=True, verbose_name="希望駐車場コード")
    target_parking_lot_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="希望駐車場名")
    target_city_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="希望市区町村コード")
    target_city_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="希望市区町村名")
    target_aza_code = models.CharField(max_length=12, blank=True, null=True, verbose_name="希望町丁目コード")
    target_aza_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="希望町丁目名")
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

    def target(self):
        """希望エリア／駐車場

        :return:
        """
        return self.target_parking_lot_name or self.target_city_name or self.target_aza_name or ''

    target.short_description = "希望エリア／駐車場"


class Waiting(BaseModel):
    target_parking_lot_code = models.IntegerField(blank=True, null=True, verbose_name="希望駐車場コード")
    target_parking_lot_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="希望駐車場名")
    target_city_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="希望市区町村コード")
    target_city_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="希望市区町村名")
    target_aza_code = models.CharField(max_length=12, blank=True, null=True, verbose_name="希望町丁目コード")
    target_aza_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="希望町丁目名")
    parking_lots = models.ManyToManyField(ParkingLot, through='WaitingParkingLot', editable=False, verbose_name="待ち対象駐車場")
    staff = models.ForeignKey(Member, blank=True, null=True, on_delete=models.PROTECT, verbose_name="担当者")
    user_name = models.CharField(max_length=50, verbose_name="氏名")
    tel = models.CharField(max_length=20, blank=True, null=True, verbose_name="電話番号")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="携帯番号")
    address1 = models.CharField(max_length=50, blank=True, null=True, verbose_name="住所１")
    address2 = models.CharField(max_length=50, blank=True, null=True, verbose_name="住所２")
    email = models.CharField(max_length=50, blank=True, null=True, verbose_name="メール")
    contractor = models.ForeignKey(Contractor, blank=True, null=True, verbose_name="契約者")
    contractor_comment = models.CharField(max_length=100, blank=True, null=True, verbose_name="契約者の備考")
    # 車情報
    car_maker = models.CharField(max_length=30, blank=True, null=True, verbose_name="メーカー")
    car_model = models.CharField(max_length=50, blank=True, null=True, verbose_name="車種")
    length = models.IntegerField(blank=True, null=True, verbose_name="全長")
    width = models.IntegerField(blank=True, null=True, verbose_name="全幅")
    height = models.IntegerField(blank=True, null=True, verbose_name="全高")
    weight = models.IntegerField(blank=True, null=True, verbose_name="重量")
    media = models.ForeignKey(TransmissionRoute, blank=True, null=True, verbose_name="媒体")
    price_handbill = models.CharField(max_length=30, blank=True, null=True, verbose_name="チラシ価格")
    created_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="入力者")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="AP備考・特記")
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_WAITING_STATUS, verbose_name="状態")
    contacts = GenericRelation(ContactHistory, related_query_name='waiting_set')

    class Meta:
        db_table = 'ap_waiting_list'
        verbose_name = "空き待ち"
        verbose_name_plural = "空き待ちリスト"

    def __str__(self):
        return "%s-%s" % (self.user_name, self.target_parking_lot_name or self.target_city_name or self.target_aza_name)

    def target(self):
        """希望エリア／駐車場

        :return:
        """
        return self.target_parking_lot_name or self.target_city_name or self.target_aza_name or ''

    target.short_description = "希望エリア／駐車場"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Waiting, self).save(force_insert, force_update, using, update_fields)
        # 既存の空き待ち情報を消す
        WaitingParkingLot.objects.public_filter(waiting=self).delete()
        # 希望駐車場の場合
        if self.target_parking_lot_code:
            try:
                parking_lot = ParkingLot.objects.get(pk=self.target_parking_lot_code)
                WaitingParkingLot.objects.create(waiting=self, parking_lot=parking_lot)
            except ObjectDoesNotExist:
                pass
        # 希望市区町村
        if self.target_city_code:
            try:
                polygon = City.objects.get(code=self.target_city_code).mpoly
                queryset = ParkingLot.objects.public_filter(point__intersects=polygon)
                for parking_lot in queryset:
                    WaitingParkingLot.objects.create(waiting=self, parking_lot=parking_lot)
            except ObjectDoesNotExist:
                pass
        # 希望町丁目
        if self.target_aza_code:
            try:
                polygon = Aza.objects.get(code=self.target_aza_code).mpoly
                queryset = ParkingLot.objects.public_filter(point__intersects=polygon)
                for parking_lot in queryset:
                    WaitingParkingLot.objects.create(waiting=self, parking_lot=parking_lot)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                pass


class WaitingContact(BaseModel):
    waiting = models.ForeignKey(Waiting, verbose_name="空き待ち")
    contact_date = models.DateField(verbose_name="連絡日")
    contact_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="連絡者")
    comment = models.CharField(max_length=255, verbose_name="備考・特記")

    class Meta:
        db_table = 'ap_waiting_contact'
        verbose_name = "連絡履歴"
        verbose_name_plural = "連絡リスト"

    def __str__(self):
        return self.comment

    def get_contact_user_name(self):
        if self.contact_user.first_name or self.contact_user.last_name:
            return '%s %s' % ((self.contact_user.last_name or ''), (self.contact_user.first_name or ''))
        else:
            return self.contact_user.username


class WaitingParkingLot(BaseModel):
    waiting = models.ForeignKey(Waiting, verbose_name="空き待ち")
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")

    class Meta:
        db_table = 'ap_waiting_parking_lot'
        verbose_name = "空き駐車場"
        verbose_name_plural = "空き駐車場一覧"


class HandbillCompany(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="業者名称")
    unit_price = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="配布単価")
    distribute_count = models.IntegerField(default=0, verbose_name="配布枚数")

    class Meta:
        db_table = 'ap_handbill_company'
        verbose_name = "チラシ業者"
        verbose_name_plural = "チラシ業者一覧"

    def __str__(self):
        return self.name


# class HandbillDistribution(BaseModel):
#     handbill_company = models.ForeignKey(HandbillCompany, verbose_name="チラシ業者")
#     unit_price = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="配布単価")
#     distribute_count = models.IntegerField(verbose_name="配布枚数")


class Trouble(BaseModel):
    trouble_date = models.DateField(verbose_name="発生日")
    inquiry_source = models.CharField(max_length=50, verbose_name="問い合わせ元")
    parking_lot = models.ForeignKey(ParkingLot, verbose_name="駐車場")
    parking_positions = models.CharField(max_length=100, blank=True, null=True,
                                         validators=[validate_comma_separated_integer_list], verbose_name="車室")
    is_all = models.BooleanField(default=False, verbose_name="全件")
    created_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="受付者")
    status = models.CharField(max_length=2, choices=constants.CHOICE_TROUBLE_STATUS, default='01', verbose_name="状態")

    class Meta:
        db_table = 'ap_trouble'
        verbose_name = "トラブル"
        verbose_name_plural = "トラブル一覧"

    def __str__(self):
        return str(self.parking_lot)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk:
            is_add = False
        else:
            is_add = True
        if not self.is_all and not self.parking_positions:
            raise errors.CustomException(constants.ERROR_PARKING_LOT_CANCELLATION_NO_POSITIONS)
        super(Trouble, self).save(force_insert, force_update, using, update_fields)
        if is_add:
            # 新規の場合、トラブル対象の車室を新規追加する。
            if self.is_all:
                parking_positions = ParkingPosition.objects.public_filter(parking_lot=self.parking_lot)
            else:
                parking_positions = ParkingPosition.objects.public_filter(pk__in=self.parking_positions.split(','))
            for parking_position in parking_positions:
                contract = parking_position.get_current_contract()
                TroublePosition.objects.create(
                    trouble=self,
                    parking_lot=self.parking_lot,
                    parking_position=parking_position,
                    contract=contract,
                    contractor=contract.contractor,
                )


class TroublePosition(BaseModel):
    trouble = models.ForeignKey(Trouble, verbose_name="トラブル")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室")
    contract = models.OneToOneField(Contract, on_delete=models.PROTECT, verbose_name="契約情報")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")

    class Meta:
        db_table = 'ap_trouble_position'
        verbose_name = "トラブルの車室"
        verbose_name_plural = "トラブルの車室一覧"

    def __str__(self):
        return '%s-%s' % (str(self.trouble), str(self.parking_position))
