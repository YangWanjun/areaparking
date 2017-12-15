from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from utils import errors, constants
from utils.django_base import BaseModel


# Create your models here.
class BaseReport(BaseModel):
    name = models.CharField(max_length=50, verbose_name="名称")
    content = models.TextField(verbose_name="内容")
    is_default = models.BooleanField(default=False, editable=False, verbose_name="デフォルト")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ReportSubscriptionConfirm(BaseReport):

    class Meta:
        db_table = 'mst_report_subscription_confirm'
        ordering = ['name']
        verbose_name = "申込確認書"
        verbose_name_plural = u"申込確認書一覧"

    @classmethod
    def get_default_report(cls):
        """デフォルトの申込確認書テンプレートを取得する。

        :return:
        """
        try:
            return ReportSubscriptionConfirm.objects.get(is_default=True)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            report = ReportSubscriptionConfirm.objects.public_all().first()
            if report is None:
                raise errors.SettingException(constants.ERROR_SETTING_NO_SUBSCRIPTION_CONFIRM)
            return report


class ReportSubscription(BaseReport):

    class Meta:
        db_table = 'mst_report_subscription'
        ordering = ['name']
        verbose_name = "申込書"
        verbose_name_plural = u"申込書一覧"

    @classmethod
    def get_default_report(cls):
        """デフォルトの申込書テンプレートを取得する。

        :return:
        """
        try:
            return ReportSubscription.objects.get(is_default=True)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            report = ReportSubscription.objects.public_all().first()
            if report is None:
                raise errors.SettingException(constants.ERROR_SETTING_NO_SUBSCRIPTION)
            return report
