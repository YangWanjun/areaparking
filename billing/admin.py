from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.TransferHeader)
class TransferHeaderAdmin(BaseAdmin):
    icon = '<i class="material-icons">attach_money</i>'
    list_display = ('company_name', 'transfer_md', 'bank_name', 'branch_name')


@admin.register(models.TransferDetail)
class TransferDetailAdmin(BaseAdmin):
    icon = '<i class="material-icons">attach_money</i>'
    list_display = ('account_number', 'account_holder', 'amount')
