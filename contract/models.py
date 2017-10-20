# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core. validators import RegexValidator

from utils.django_base import BaseModel
from utils import constants

# Create your models here.
class Contractor(BaseModel):
    number = models.IntegerField(
        verbose_name="契約者No.", unique=True,
        validators=(RegexValidator(regex=r'^\d{8}$'),)
    )
    name = models.CharField(max_length=15, verbose_name="名前")
    kana = models.CharField(max_length=15, verbose_name="カナ")
    segment = models.CharField(max_length=1, choices=constants.CHOICE_CONTRACTOR_TYPE, verbose_name="契約者分類")
    gender = models.CharField(max_length=1, choices=constants.CHOICE_GENDER, verbose_name="性別")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")
    email = models.EmailField(blank=True, null=True, verbose_name="メールアドレス")
    birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")
