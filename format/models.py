import os

from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.storage import FileSystemStorage
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from utils import errors, constants, common
from utils.django_base import BaseModel


# Create your models here.
class ReportFileStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        return name


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


class ReportContract(BaseReport):

    class Meta:
        db_table = 'mst_report_contract'
        ordering = ['name']
        verbose_name = "契約書"
        verbose_name_plural = u"契約書一覧"

    @classmethod
    def get_default_report(cls):
        """デフォルトの契約書テンプレートを取得する。

        :return:
        """
        try:
            return ReportSubscription.objects.get(is_default=True)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            report = ReportSubscription.objects.public_all().first()
            if report is None:
                raise errors.SettingException(constants.ERROR_SETTING_NO_SUBSCRIPTION)
            return report


class ReportFile(BaseModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=50, verbose_name="帳票名称")
    path = models.FileField(upload_to=common.get_report_path)

    class Meta:
        db_table = 'ap_report_file'
        verbose_name = "帳票ファイル"
        verbose_name_plural = u"帳票ファイル一覧"

    def __str__(self):
        return os.path.basename(str(self.path))

    def delete(self, using=None, keep_parents=False):
        if os.path.exists(self.path.path):
            os.remove(self.path.path)
        super(ReportFile, self).delete(using, keep_parents)
