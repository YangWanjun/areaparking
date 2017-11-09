# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.BkMst)
class BkMstAdmin(BaseAdmin):
    icon = '<i class="material-icons">local_parking</i>'
    list_display = ('bk_no', 'bk_name', 'brui', 'address', 'tanto', 'kosin_user')
    list_display_links = ('bk_no', 'bk_name')
    search_fields = ('bk_no', 'bk_name')
    list_filter = (
        ('tanto', admin.RelatedOnlyFieldListFilter),
    )


@admin.register(models.HyMst)
class HyMstAdmin(BaseAdmin):
    list_display = ('bk_no', 'hy_no')
    list_display_links = ('bk_no', 'hy_no')
    search_fields = ('bk_no', 'hy_no')


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


@admin.register(models.KysMst)
class KysMstAdmin(BaseAdmin):
    icon = '<i class="material-icons">nature_people</i>'
    list_display = ('kys_no', 'kys_name', 'kys_rui', 'email')
    list_display_links = ('kys_no', 'kys_name',)


@admin.register(models.MKinyu)
class MKinyuAdmin(BaseAdmin):
    list_display = ('kinyu_no', 'kinyu_name', 'tel1', 'tel2')
    list_display_links = ('kinyu_no', 'kinyu_name',)


@admin.register(models.MTen)
class MTenAdmin(BaseAdmin):
    list_display = ('kinyu_no', 'ten_no', 'ten_name')
    list_display_links = ('ten_no', 'ten_name',)


@admin.register(models.MKozaFuri)
class MKozaFuriAdmin(BaseAdmin):
    list_display = ('fkae_no', 'fkae_name', 'kinyu_no', 'ten_no')
    list_display_links = ('fkae_no', 'fkae_name',)
