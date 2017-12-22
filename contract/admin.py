# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models, forms
from utils.django_base import BaseAdmin


# Register your models here.
class ContractorCarInline(admin.TabularInline):
    model = models.ContractorCar
    extra = 0


class ContractPaymentInline(admin.TabularInline):
    model = models.ContractPayment
    extra = 0


@admin.register(models.Contractor)
class ContractorAdmin(BaseAdmin):
    icon = '<i class="material-icons">nature_people</i>'
    list_display = ('code', 'name', 'category', 'address1', 'address2')
    list_display_links = ('code', 'name')
    search_fields = ('code', 'name')
    inlines = (ContractorCarInline,)
    form = forms.ContractorForm
    fieldsets = (
        (None, {
            'fields': (
                'category',
                ('name', 'kana',),
                'post_code',
                ('address1', 'address2'),
                ('tel', 'fax',),
                'email',
                'comment',
            )
        }),
        ("個人情報", {
            'classes': ('collapse',),
            'fields': (
                ('personal_gender', 'personal_birthday', ),
            )
        }),
        ("法人情報", {
            'classes': ('collapse',),
            'fields': (
                ('corporate_business_type', ),
                ('corporate_president', 'corporate_web_site'),
                ('corporate_staff_name', 'corporate_staff_department', 'corporate_staff_position'),
                ('corporate_capital', 'corporate_turnover'),
            )
        }),
        ("勤務先", {
            'classes': ('collapse',),
            'fields': (
                'workplace_name',
                'workplace_post_code',
                ('workplace_address1', 'workplace_address2'),
                ('workplace_tel', 'workplace_fax'),
            )
        }),
        ("連絡先", {
            'classes': ('collapse',),
            'fields': (
                ('contact_name', 'contact_kana',),
                'contact_post_code',
                ('contact_address1', 'contact_address2',),
                ('contact_tel', 'contact_fax',),
                'contact_relation',
            )
        }),
        ("書類送付先", {
            'classes': ('collapse',),
            'fields': (
                'delivery_type',
                'delivery_honorific',
                ('delivery_name', 'delivery_kana',),
                'delivery_post_code',
                ('delivery_address1', 'delivery_address2'),
                ('delivery_tel', 'delivery_fax'),
            )
        }),
        ("保証人", {
            'classes': ('collapse',),
            'fields': (
                ('guarantor_name', 'guarantor_kana'),
                'guarantor_birthday',
                'guarantor_post_code',
                ('guarantor_address1', 'guarantor_address2'),
                ('guarantor_tel', 'guarantor_fax'),
                'guarantor_relation',
                'guarantor_comment',
            )
        })
    )


@admin.register(models.Contract)
class ContractAdmin(BaseAdmin):
    list_display = ('contractor', 'parking_lot', 'parking_position', 'contract_date', 'start_date', 'end_date')
    list_display_links = ('contractor',)
    inlines = (ContractPaymentInline,)
    form = forms.ContractForm
