from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.ReportSubscription)
class ReportSubscription(BaseAdmin):
    save_as = True

    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/tinymce.init.js',
        )
