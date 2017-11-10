# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin

# Register your models here.

@admin.register(models.Company)
class CompanyAdmin(BaseAdmin):

    def has_add_permission(self, request):
        if models.Company.objects.public_all().count() > 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(models.ParkingLotType)
# class ParkingLotTypeAdmin(BaseAdmin):
#     list_display = ('code', 'name')
#     list_display_links = ('code', 'name')


@admin.register(models.ParkingTimeLimit)
class ParkingTimeLimitAdmin(BaseAdmin):
    pass


# @admin.register(models.BankCode)
# class BankCodeAdmin(BaseAdmin):
#     pass


# @admin.register(models.ManagementType)
# class ManagementTypeAdmin(BaseAdmin):
#     list_display = ('code', 'name')
#     list_display_links = ('code', 'name')


@admin.register(models.CarMaker)
class CarMakerAdmin(BaseAdmin):
    pass


@admin.register(models.CarModel)
class CarModelAdmin(BaseAdmin):
    list_display = ('maker', 'name', 'grade_name', 'sale_date',
                    'length', 'width', 'height', 'weight')
    search_fields = ('maker__name', 'name', 'grade_name')


# @admin.register(models.Bank)
# class BankAdmin(BaseAdmin):
#     list_display = ('bank_name', 'branch_no', 'branch_name', 'account_type', 'account_number', 'account_holder')


@admin.register(models.TransmissionRoute)
class TransmissionRouteAdmin(BaseAdmin):
    pass
