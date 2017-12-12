from django.contrib import admin

from . import models
from utils.django_base import BaseAdmin


# Register your models here.
@admin.register(models.ReportSubscription)
class ReportSubscription(BaseAdmin):
    pass
