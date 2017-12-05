from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
class MemberShipDocInline(admin.TabularInline):
    model = models.MemberShip
    extra = 0


@admin.register(models.Department)
class DepartmentAdmin(BaseAdmin):
    pass


@admin.register(models.Member)
class MemberAdmin(BaseAdmin):
    list_display = ('first_name', 'last_name', 'join_date', 'email', 'is_retired')
    inlines = (MemberShipDocInline,)
