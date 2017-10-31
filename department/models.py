# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utils.django_base import BaseModel
from utils import constants


# Create your models here.
class Department(BaseModel):
    name = models.CharField(max_length=30, verbose_name="名称")

    class Meta:
        db_table = 'ap_department'
        ordering = ['name']
        verbose_name = "部署"
        verbose_name_plural = "部署一覧"

    def __unicode__(self):
        return self.name


class Member(BaseModel):
    first_name = models.CharField(max_length=30, verbose_name=u"姓")
    last_name = models.CharField(max_length=30, verbose_name=u"名")
    gender = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_GENDER, verbose_name=u"性別")
    birthday = models.DateField(blank=True, null=True, verbose_name=u"生年月日")
    join_date = models.DateField(blank=True, null=True, verbose_name=u"入社年月日")
    email = models.EmailField(blank=True, null=True, verbose_name=u"会社メールアドレス")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号",
                                 help_text=u"数値だけを入力してください、例：1230034")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号",
                             help_text=u"数値だけを入力してください、例：08012345678")
    marriage = models.CharField(blank=True, null=True, max_length=1,
                                choices=constants.CHOICE_MARRIED, verbose_name=u"婚姻状況")
    is_retired = models.BooleanField(default=False, verbose_name=u"退職")
    retired_date = models.DateField(blank=True, null=True, verbose_name=u"退職年月日")

    class Meta:
        db_table = 'ap_member'
        ordering = ['first_name', 'last_name']
        verbose_name = "社員"
        verbose_name_plural = "社員一覧"

    def __unicode__(self):
        return "{} {}".format(self.first_name, self.last_name)
