# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.BkMst)
class BkMstAdmin(BaseAdmin):
    list_display = ('bk_no', 'bk_name', 'brui', 'address', 'tanto', 'kosin_user')
    list_display_links = ('bk_no', 'bk_name')
    search_fields = ('bk_no', 'bk_name')
    list_filter = (
        ('tanto', admin.RelatedOnlyFieldListFilter),
    )


@admin.register(models.BaiRooms)
class BaiRoomsAdmin(BaseAdmin):
    list_display = ('buken', 'naibu_no', 'hy_no', 'biko', 'kosin_user')
    list_display_links = ('buken', 'naibu_no', 'hy_no')
    search_fields = ('buken__bk_no', 'buken__bk_name')


@admin.register(models.MBrui)
class MBruiAdmin(BaseAdmin):
    list_display = ('brui_no', 'brui_name', 'biko', 'kosin_user')
    list_display_links = ('brui_no', 'brui_name',)


@admin.register(models.MTanto)
class MTantoAdmin(BaseAdmin):
    list_display = ('tanto_no', 'tanto_name', 'email', 'biko', 'busyo', 'kosin_user')
    list_display_links = ('tanto_no', 'tanto_name',)


@admin.register(models.BaiMBusyo)
class BaiMBusyoAdmin(BaseAdmin):
    list_display = ('busyo_no', 'busyo_name', 'busyo_biko', 'kosin_user')
    list_display_links = ('busyo_no', 'busyo_name',)
