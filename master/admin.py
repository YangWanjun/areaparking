# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models, forms
from utils.django_base import BaseAdmin, BaseAdminEditor


# Register your models here.
class MailCcListInline(admin.TabularInline):
    model = models.MailCcList
    extra = 1


@admin.register(models.Config)
class ConfigAdmin(BaseAdmin):
    form = forms.ConfigForm
    list_display = ('group', 'name', 'value')
    list_display_links = ('name',)


@admin.register(models.Company)
class CompanyAdmin(BaseAdmin):

    def has_add_permission(self, request):
        if models.Company.objects.public_all().count() > 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.CarMaker)
class CarMakerAdmin(BaseAdmin):
    pass


@admin.register(models.CarModel)
class CarModelAdmin(BaseAdmin):
    list_display = ('maker', 'name', 'grade_name', 'sale_date',
                    'length', 'width', 'height', 'weight')
    search_fields = ('maker__name', 'name', 'grade_name')


@admin.register(models.Bank)
class BankAdmin(BaseAdmin):
    pass


@admin.register(models.BankAccount)
class BankAccountAdmin(BaseAdmin):
    list_display = ('bank', 'branch_no', 'branch_name', 'account_type', 'account_number', 'account_holder')


@admin.register(models.TransmissionRoute)
class TransmissionRouteAdmin(BaseAdmin):
    list_display = ('name', 'price_kbn')


@admin.register(models.Payment)
class PaymentAdmin(BaseAdmin):
    list_display = ('name', 'timing', 'amount', 'consumption_tax_kbn', 'is_active')


@admin.register(models.Mediation)
class MediationAdmin(BaseAdmin):
    pass


@admin.register(models.MailTemplate)
class MailTemplateAdmin(BaseAdminEditor):
    pass


@admin.register(models.MailGroup)
class MailGroupAdmin(BaseAdmin):
    list_display = ('code', 'name', 'sender', 'template')
    inlines = (MailCcListInline,)
