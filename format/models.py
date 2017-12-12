from django.db import models

# from tinymce.models import HTMLField

from utils.django_base import BaseModel


# Create your models here.
class BaseReport(BaseModel):
    name = models.CharField(max_length=50, verbose_name=u"名称")
    content = models.TextField(verbose_name="内容")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ReportSubscription(BaseReport):

    class Meta:
        db_table = 'mst_report_subscription'
        ordering = ['name']
        verbose_name = "申込書"
        verbose_name_plural = u"申込書一覧"

