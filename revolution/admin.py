# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.BkMst)
class BkMstAdmin(BaseAdmin):
    pass


@admin.register(models.BaiRooms)
class BaiRoomsAdmin(BaseAdmin):
    pass
