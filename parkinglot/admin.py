# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
from utils import constants
from utils.django_base import BaseAdmin


# Register your models here.
class ParkingPositionInline(admin.TabularInline):
    model = models.ParkingPosition
    extra = 1


@admin.register(models.ParkingLot)
class ParkingLotAdmin(BaseAdmin):
    icon = '<i class="material-icons">local_parking</i>'
    list_display = ('code', 'name', 'segment', 'pref_name', 'city_name', 'town_name')
    list_display_links = ('name',)
    search_fields = ('code', 'name')
    fields = (
        'code',
        ('name', 'kana'),
        'segment',
        'post_code',
        ('pref_code', 'pref_name', 'city_code', 'city_name'),
        ('town_name', 'aza_name', 'other_name'),
        ('lon', 'lat'),
        'traffic',
        ('car_count', 'bike_count'),
        'comment'
    )
    inlines = (ParkingPositionInline,)


@admin.register(models.ParkingPosition)
class ParkingPosition(BaseAdmin):
    list_display = ('parking_plot', 'name', 'price_recruitment_no_tax', 'price_homepage_no_tax', 'price_handbill_no_tax',
                    'length', 'width', 'height', 'weight')
    list_display_links = ('name',)
    search_fields = ('parking_plot__code', 'parking_plot__name')
    fieldsets = (
        (None, {
            'fields': (
                ('parking_plot',),
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
    # fields = (
    #     ('parking_plot',),
    #     'name',
    #     ('length', 'width', 'height', 'weight'),
    #     ('tyre_width', 'tyre_width_ap', 'min_height', 'min_height_ap'),
    #     ('f_value', 'r_value', ),
    #     'time_limit',
    #     'comment'
    # )


admin.site.site_header = constants.SYSTEM_NAME
admin.site.site_title = constants.SYSTEM_NAME
