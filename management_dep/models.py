from django.db import models
from django.utils.functional import cached_property

from contract.models import Contract, Contractor, Subscription
from master.models import Bank, BankAccount
from parkinglot.models import ParkingLot, ParkingPosition
from utils import constants
from utils.django_base import BaseViewModel


# Create your models here.
class VBankAccount(BaseViewModel):
    bank = models.ForeignKey(Bank, verbose_name="銀行")
    branch_no = models.CharField(max_length=7, verbose_name="支店番号")
    branch_name = models.CharField(max_length=20, verbose_name="支店名称")
    account_type = models.CharField(max_length=1, choices=constants.CHOICE_BANK_ACCOUNT_TYPE, verbose_name="預金種類")
    account_number = models.CharField(max_length=7, verbose_name="口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=30, verbose_name="口座名義")
    contract = models.ForeignKey(Contract, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="契約")
    parking_lot = models.ForeignKey(ParkingLot, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, blank=True, null=True, on_delete=models.DO_NOTHING,
                                         verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="契約者")
    subscription = models.ForeignKey(Subscription, blank=True, null=True, on_delete=models.DO_NOTHING,
                                     verbose_name="申込者")
    status = models.CharField(max_length=1, choices=constants.CHOICE_BANK_ACCOUNT_STATUS, verbose_name="状態")

    class Meta:
        managed = False
        db_table = 'v_bank_account'
        verbose_name = "口座"
        verbose_name_plural = "口座利用一覧"

    def __str__(self):
        return self.account_number

    @cached_property
    def bank_account(self):
        return BankAccount.objects.get(pk=self.pk)


