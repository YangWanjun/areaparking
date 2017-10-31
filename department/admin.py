# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.Department)
class DepartmentAdmin(BaseAdmin):
    pass


@admin.register(models.Member)
class MemberAdmin(BaseAdmin):
    list_display = ('__unicode__', 'join_date', 'email', 'phone')
