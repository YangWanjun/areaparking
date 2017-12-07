# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models, forms
from utils import constants
from utils.django_base import BaseAdmin


# Register your models here.
class ParkingPositionInline(admin.TabularInline):
    model = models.ParkingPosition
    extra = 0


class ParkingLotDocInline(admin.TabularInline):
    model = models.ParkingLotDoc
    extra = 1


class ParkingLotCommentInline(admin.TabularInline):
    model = models.ParkingLotComment
    extra = 1


class ParkingLotStaffHistoryInline(admin.TabularInline):
    model = models.ParkingLotStaffHistory
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ParkingPositionKeyInline(admin.TabularInline):
    model = models.ParkingPositionKey
    extra = 0


@admin.register(models.ParkingLotType)
class ParkingLotTypeAdmin(BaseAdmin):
    list_display = ('code', 'name')
    list_display_links = ('code', 'name')


@admin.register(models.ParkingTimeLimit)
class ParkingTimeLimitAdmin(BaseAdmin):
    pass


@admin.register(models.LeaseManagementCompany)
class LeaseManagementCompanyAdmin(BaseAdmin):
    list_display = ('name', 'department', 'position', 'staff', 'address', 'tel', 'email')


@admin.register(models.BuildingManagementCompany)
class BuildingManagementCompanyAdmin(BaseAdmin):
    list_display = ('name', 'department', 'position', 'staff', 'address', 'tel', 'email')


@admin.register(models.TryPuttingOperator)
class TryPuttingOperatorAdmin(BaseAdmin):
    pass


@admin.register(models.ParkingLot)
class ParkingLotAdmin(BaseAdmin):
    form = forms.ParkingLotForm
    icon = '<i class="material-icons">local_parking</i>'
    list_display = ('code', 'name', 'category', 'address')
    search_fields = ('code', 'name',)
    inlines = (ParkingLotCommentInline, ParkingLotStaffHistoryInline, ParkingLotDocInline, ParkingPositionInline,)

    def address(self, obj):
        return obj.address()

    address.short_description = "所在地"


@admin.register(models.ParkingPosition)
class ParkingPosition(BaseAdmin):
    form = forms.ParkingPositionForm
    list_display = ('parking_lot', 'name', 'length', 'width', 'height', 'weight')
    list_display_links = ('parking_lot', 'name',)
    search_fields = ('parking_lot__code', 'parking_lot__name')
    fieldsets = (
        (None, {
            'fields': (
                ('parking_lot',),
                'name',
            )
        }),
        ("賃料", {
            'classes': ('collapse',),
            'fields': (
                ('price_recruitment', 'price_recruitment_no_tax'),
                ('price_homepage', 'price_homepage_no_tax'),
                ('price_handbill', 'price_handbill_no_tax',),
            )
        }),
        ("サイズ", {
            'classes': ('collapse',),
            'fields': (
                ('length', 'width', 'height', 'weight'),
                ('tyre_width', 'tyre_width_ap', 'min_height', 'min_height_ap'),
                ('f_value', 'r_value',),
            )
        }),
        ('備考', {
            'fields': (
                'comment',
            )
        }),
    )
    inlines = (ParkingPositionKeyInline,)


admin.site.site_header = constants.SYSTEM_NAME
admin.site.site_title = constants.SYSTEM_NAME
