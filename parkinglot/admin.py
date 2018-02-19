# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models, forms
from address.biz import geocode
from utils.django_base import BaseAdmin


# Register your models here.
class ParkingPositionInline(admin.TabularInline):
    model = models.ParkingPosition
    extra = 0


class ParkingLotDocInline(admin.TabularInline):
    model = models.ParkingLotDoc
    form = forms.ParkingLotDocForm
    extra = 1


class ParkingLotImageInline(admin.TabularInline):
    model = models.ParkingLotImage
    extra = 1


class ParkingLotCommentInline(admin.TabularInline):
    model = models.ParkingLotComment
    extra = 1


class ParkingLotKeyInline(admin.TabularInline):
    model = models.ParkingLotKey
    extra = 0


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
    inlines = (ParkingLotCommentInline, ParkingLotStaffHistoryInline, ParkingLotDocInline, ParkingLotImageInline,
               ParkingLotKeyInline)

    def save_model(self, request, obj, form, change):
        if change is False or (
            'pref_name' in form.changed_data or
            'city_name' in form.changed_data or
            'town_name' in form.changed_data or
            'aza_name' in form.changed_data or
            'other_name' in form.changed_data
        ):
            # 新規の場合、または住所変更した場合、座標を取得しなおします。
            coordinate = geocode(obj.address)
            if coordinate.get('lng', None):
                obj.lng = coordinate.get('lng', None)
            if coordinate.get('lat', None):
                obj.lat = coordinate.get('lat', None)
            if coordinate.get('post_code', None):
                obj.post_code = coordinate.get('post_code', None)
        super(ParkingLotAdmin, self).save_model(request, obj, form, change)


@admin.register(models.ParkingPosition)
class ParkingPosition(BaseAdmin):
    form = forms.ParkingPositionForm
    list_display = ('parking_lot', 'name', 'length', 'width', 'height', 'weight')
    list_display_links = ('parking_lot', 'name',)
    search_fields = ('parking_lot__code', 'parking_lot__name')
    fieldsets = (
        (None, {
            'fields': (
                'parking_lot',
                'name', 'category',
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
    save_as = True
