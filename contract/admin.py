# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models, forms
from utils import constants
from utils.django_base import BaseAdmin

# Register your models here.

@admin.register(models.Contractor)
class ContractorAdmin(BaseAdmin):
    icon = '<i class="material-icons">nature_people</i>'
    list_display = ('code', 'name', 'segment', 'personal_address1', 'personal_address2')
    list_display_links = ('code', 'name')
    search_fields = ('code', 'name')
    form = forms.ContractorForm
    fieldsets = (
        (None, {'fields': ('code', 'segment')}),
        ("個人情報", {
            'classes': ('collapse',),
            'fields': (
                ('name', 'kana', ),
                ('gender', 'personal_birthday', ),
                'personal_post_code',
                ('personal_address1', 'personal_address2'),
                ('personal_tel', 'personal_fax',),
                'personal_email',
                'personal_comment',
            )
        }),
        ("法人情報", {
            'classes': ('collapse',),
            'fields': (
                ('business_type', ),
                ('president', 'web_site'),
                ('staff_name', 'staff_department', 'position', 'extension'),
                ('capital', 'turnover'),
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
                'paper_delivery_type',
                'honorific',
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
