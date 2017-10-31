# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from parkinglot.models import ParkingLot, ParkingPosition
from contract.models import Contractor
from utils.django_base import BaseModel

# Create your models here.
class TempContract(BaseModel):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.PROTECT, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, on_delete=models.PROTECT, verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
    contract_date = models.DateField(blank=True, null=True, verbose_name="契約日")
    start_date = models.DateField(blank=True, null=True, verbose_name="契約開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name="契約終了日")
    pay_date = models.DateField(blank=True, null=True, verbose_name="賃料発生日",
                                help_text="未入力の場合、契約期間の開始日が賃料発生日として扱われます")

    class Meta:
        db_table = 'ap_temp_contract'
        ordering = ['contractor', 'start_date']
        verbose_name = "仮契約情報"
        verbose_name_plural = "仮契約情報一覧"

    def __unicode__(self):
        return str(self.pk)
