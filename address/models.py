from django.contrib.gis.db import models
from django.core.validators import RegexValidator, validate_comma_separated_integer_list

from utils.django_base import BaseModel


# Create your models here.
class Pref(BaseModel):
    code = models.CharField(max_length=2, primary_key=True, verbose_name="都道府県コード")
    name = models.CharField(max_length=20, unique=True, verbose_name="都道府県名称")

    class Meta:
        db_table = 'gis_pref'
        ordering = ['code']
        verbose_name = "都道府県"
        verbose_name_plural = "都道府県一覧"

    def __str__(self):
        return self.name


class City(BaseModel):
    code = models.CharField(max_length=5, primary_key=True, verbose_name="市区町村コード")
    name = models.CharField(max_length=30, verbose_name="市区町村名称")
    name_en = models.CharField(max_length=30, blank=True, null=True, verbose_name="市区町村名（英語）")
    pref = models.ForeignKey(Pref, verbose_name="都道府県")
    mpoly = models.MultiPolygonField(srid=4326, blank=True, null=True)
    people_count = models.IntegerField(blank=True, null=True, verbose_name="人口")
    home_count = models.IntegerField(blank=True, null=True, verbose_name="世帯数")

    class Meta:
        db_table = 'gis_city'
        ordering = ['code']
        verbose_name = "市区町村"
        verbose_name_plural = "市区町村一覧"

    def __str__(self):
        return self.name


class Aza(BaseModel):
    code = models.CharField(max_length=12, verbose_name="大字町丁目コード")
    name = models.CharField(max_length=30, verbose_name="大字町丁目名称")
    city = models.ForeignKey(City, verbose_name="市区町村")
    pref = models.ForeignKey(Pref, verbose_name="都道府県")
    point = models.PointField(blank=True, null=True, verbose_name="座標")
    full_name = models.CharField(max_length=120, verbose_name="名称")
    mpoly = models.MultiPolygonField(srid=4326, blank=True, null=True)
    people_count = models.IntegerField(blank=True, null=True, verbose_name="人口")
    home_count = models.IntegerField(blank=True, null=True, verbose_name="世帯数")


    class Meta:
        db_table = 'gis_aza'
        ordering = ['code']
        verbose_name = "大字町丁目"
        verbose_name_plural = "大字町丁目一覧"

    def __str__(self):
        return self.name


class Postcode(BaseModel):
    city_code = models.CharField(
        max_length=5, validators=(RegexValidator(regex=r"^\d{5}$"),), verbose_name=u"市区町村コード"
    )
    post_code = models.CharField(
        max_length=7, validators=(RegexValidator(regex=r"^\d{7}$"),), verbose_name=u"郵便番号"
    )
    pref_name = models.CharField(max_length=15, verbose_name="都道府県名称")
    city_name = models.CharField(max_length=50, verbose_name="市区町村名称")
    town_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="町域名称")
    pref_kana = models.CharField(max_length=50, verbose_name="度道府県カナ")
    city_kana = models.CharField(max_length=50, verbose_name="市区町村カナ")
    town_kana = models.CharField(max_length=100, blank=True, null=True, verbose_name="町域カナ")
    chome_list = models.CharField(
        max_length=200, blank=True, null=True,
        validators=[validate_comma_separated_integer_list], verbose_name="丁目リスト"
    )
    is_partial = models.BooleanField(
        default=False, verbose_name="町域の一部",
        help_text="一町域が二以上の郵便番号で表される場合の表示（「1」は該当、「0」は該当せず）"
    )
    is_multi_chome = models.BooleanField(
        default=False, verbose_name="複数の丁目",
        help_text="丁目を有する町域の場合の表示（「1」は該当、「0」は該当せず）"
    )
    is_multi_town = models.BooleanField(
        default=False, verbose_name="複数町域あり",
        help_text="一つの郵便番号で二以上の町域を表す場合の表示（「1」は該当、「0」は該当せず）"
    )

    class Meta:
        db_table = 'gis_post_code'
        verbose_name = "郵便番号"
        verbose_name_plural = '郵便番号一覧'

    def __str__(self):
        return self.post_code

    @property
    def address(self):
        return "{}{}{}".format(self.pref_name, self.city_name, self.town_name or '')


class AzaTest(BaseModel):
    KEY_CODE = models.CharField(max_length=11, blank=True, null=True)
    PREF = models.CharField(max_length=2, blank=True, null=True)
    CITY = models.CharField(max_length=3, blank=True, null=True)
    S_AREA = models.CharField(max_length=6, blank=True, null=True)
    PREF_NAME = models.CharField(max_length=12, blank=True, null=True)
    CITY_NAME = models.CharField(max_length=14, blank=True, null=True)
    S_NAME = models.CharField(max_length=96, blank=True, null=True)
    KIGO_E = models.CharField(max_length=3, blank=True, null=True)
    HCODE = models.IntegerField(blank=True, null=True)
    AREA = models.FloatField(blank=True, null=True)
    PERIMETER = models.FloatField(blank=True, null=True)
    H27KAxx = models.IntegerField(blank=True, null=True, db_column='H27KAxx_')
    H27KAxx_ID = models.IntegerField(blank=True, null=True)
    KEN = models.CharField(max_length=2, blank=True, null=True)
    KEN_NAME = models.CharField(max_length=12, blank=True, null=True)
    SITYO_NAME = models.CharField(max_length=22, blank=True, null=True)
    GST_NAME = models.CharField(max_length=14, blank=True, null=True)
    CSS_NAME = models.CharField(max_length=14, blank=True, null=True)
    KIHON1 = models.CharField(max_length=4, blank=True, null=True)
    DUMMY1 = models.CharField(max_length=1, blank=True, null=True)
    KIHON2 = models.CharField(max_length=2, blank=True, null=True)
    KEYCODE1 = models.CharField(max_length=9, blank=True, null=True)
    KEYCODE2 = models.CharField(max_length=9, blank=True, null=True)
    AREA_MAX_F = models.CharField(max_length=1, blank=True, null=True)
    KIGO_D = models.CharField(max_length=2, blank=True, null=True)
    N_KEN = models.CharField(max_length=2, blank=True, null=True)
    N_CITY = models.CharField(max_length=3, blank=True, null=True)
    KIGO_I = models.CharField(max_length=1, blank=True, null=True)
    MOJI = models.CharField(max_length=96, blank=True, null=True)
    KBSUM = models.IntegerField(blank=True, null=True)
    JINKO = models.BigIntegerField(blank=True, null=True)
    SETAI = models.BigIntegerField(blank=True, null=True)
    X_CODE = models.FloatField(blank=True, null=True)
    Y_CODE = models.FloatField(blank=True, null=True)
    KCODE1 = models.CharField(max_length=7, blank=True, null=True)
    mpoly = models.MultiPolygonField(srid=4326, blank=True, null=True)

    class Meta:
        db_table = 'gis_aza_test'
        verbose_name = "町丁字境界データ"
        verbose_name_plural = "町丁字境界データ"

    def __str__(self):
        return self.KEY_CODE
