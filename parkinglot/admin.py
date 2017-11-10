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


@admin.register(models.ParkingLot)
class ParkingLotAdmin(BaseAdmin):
    form = forms.ParkingLotForm
    icon = '<i class="material-icons">local_parking</i>'
    list_display = ('bk_no', 'buken', 'address', 'tanto')
    search_fields = ('buken__bk_no', 'buken__bk_name',)
    inlines = (ParkingLotDocInline, ParkingPositionInline,)
    list_filter = (
        'buken__tanto',
    )

    def bk_no(self, obj):
        return obj.buken.bk_no

    def address(self, obj):
        return obj.buken.address()

    def tanto(self, obj):
        return obj.buken.tanto

    bk_no.short_description = "物件番号"
    bk_no.admin_order_field = 'buken__bk_no'
    address.short_description = "場所"
    tanto.short_description = "担当者"
    tanto.admin_order_field = 'buken__tanto'


@admin.register(models.ParkingPosition)
class ParkingPosition(BaseAdmin):
    form = forms.ParkingPositionForm
    list_display = ('parking_lot', 'name', 'price_recruitment_no_tax', 'price_homepage_no_tax', 'price_handbill_no_tax',
                    'length', 'width', 'height', 'weight')
    list_display_links = ('parking_lot', 'name',)
    search_fields = ('parking_lot__buken__bk_no', 'parking_lot__buken__bk_name')
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
        (None, {
            'fields': (
                'time_limit',
                'comment'
            )
        }),
    )


admin.site.site_header = constants.SYSTEM_NAME
admin.site.site_title = constants.SYSTEM_NAME
