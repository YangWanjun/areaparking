from django.core.validators import RegexValidator
from django.db import models

from utils import constants
from utils.django_base import BaseModel


# Create your models here.
class Member(BaseModel):
    first_name = models.CharField(max_length=30, verbose_name="姓")
    last_name = models.CharField(max_length=30, verbose_name="名")
    gender = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_GENDER, verbose_name="性別")
    birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")
    join_date = models.DateField(blank=True, null=True, verbose_name="入社年月日")
    email = models.EmailField(blank=True, null=True, verbose_name="会社メールアドレス")
    post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name="郵便番号",
                                 validators=(RegexValidator(regex=constants.REG_POST_CODE),))
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name="住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name="住所２")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name="電話番号",
                             validators=(RegexValidator(regex=constants.REG_TEL),))
    marriage = models.CharField(blank=True, null=True, max_length=1,
                                choices=constants.CHOICE_MARRIED, verbose_name="婚姻状況")
    is_retired = models.BooleanField(default=False, verbose_name="退職")
    retired_date = models.DateField(blank=True, null=True, verbose_name="退職年月日")

    class Meta:
        db_table = 'ap_member'
        ordering = ['first_name', 'last_name']
        verbose_name = "社員"
        verbose_name_plural = "社員一覧"

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Department(BaseModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="名称")
    members = models.ManyToManyField(Member, through='MemberShip')

    class Meta:
        db_table = 'ap_department'
        ordering = ['name']
        verbose_name = "部署"
        verbose_name_plural = "部署一覧"

    def __str__(self):
        return self.name


class MemberShip(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name="社員")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="部署")
    start_date = models.DateField(verbose_name="開始日")
    end_date = models.DateField(default=constants.END_DATE, verbose_name="終了日")

    class Meta:
        db_table = 'ap_membership'
        ordering = ['department', 'member']
        verbose_name = "社員所属"
        verbose_name_plural = "社員所属一覧"

    def __str__(self):
        return "{} - {}".format(str(self.department), str(self.member))
