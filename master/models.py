# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core. validators import RegexValidator

from utils.django_base import BaseModel

# Create your models here.
class ParkingLotType(BaseModel):
    number = models.IntegerField(primary_key=True, verbose_name="駐車場分類No.",
                                 validators=(RegexValidator(regex=r'^\d{4}$'),))
    name = models.CharField(max_length=30, verbose_name="名称")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'mst_parking_lot_type'
        ordering = ['number']
        verbose_name = "駐車場分類"
        verbose_name_plural = "駐車場分類一覧"

    def __unicode__(self):
        return self.name


class ParkingTimeLimit(BaseModel):
    number = models.IntegerField(primary_key=True, verbose_name="時間制限No.",
                                 validators=(RegexValidator(regex=r'^\d{4}$'),))
    name = models.CharField(max_length=30, verbose_name="名称")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'mst_parking_time_limit'
        ordering = ['number']
        verbose_name = "駐車場分類"
        verbose_name_plural = "駐車場分類一覧"

    def __unicode__(self):
        return self.name
