from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.ReportSubscriptionConfirm)
class ReportSubscriptionConfirmAdmin(BaseAdmin):
    list_display = ('name', 'is_default')
    save_as = True
    actions = ('set_default_template',)

    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/tinymce.init.js',
        )

    def set_default_template(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "既定おテンプレートは１つしか設定できない。")
        else:
            models.ReportSubscriptionConfirm.objects.public_all().update(is_default=False)
            queryset.update(is_default=True)

    set_default_template.short_description = "既定に設定"


@admin.register(models.ReportSubscription)
class ReportSubscriptionAdmin(BaseAdmin):
    list_display = ('name', 'is_default')
    save_as = True
    actions = ('set_default_template',)

    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/tinymce.init.js',
        )

    def set_default_template(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "既定おテンプレートは１つしか設定できない。")
        else:
            models.ReportSubscription.objects.public_all().update(is_default=False)
            queryset.update(is_default=True)

    set_default_template.short_description = "既定に設定"
