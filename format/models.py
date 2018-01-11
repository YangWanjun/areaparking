import os

from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.files.storage import FileSystemStorage
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse

from utils import errors, constants, common
from utils.django_base import BaseModel


# Create your models here.
class Step(object):

    STEPS = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5, '⑥': 6, '⑦': 7, '⑧': 8}

    def __init__(self, step, name, prev_step=None, next_step=None, url_pattern=None, url_kwargs=None):
        self.step = step
        self.name = name
        self.prev_step = prev_step
        self.next_step = next_step
        self.is_finished = False
        self.url_pattern = url_pattern
        self.url_kwargs = url_kwargs

    def to_json(self, level=0):
        return {
            'full_name': self.full_name(),
            'step': self.step,
            'name': self.name,
            'prev_step': self.prev_step.to_json(1) if self.prev_step and level == 0 else None,
            'next_step': self.next_step.to_json(1) if self.next_step and level == 0 else None,
            'is_finished': self.is_finished,
            'url': self.url(),
        }

    def full_name(self):
        return '%s %s' % (self.step, self.name)

    def url(self):
        url_name = self.url_pattern % self.STEPS.get(self.step)
        return reverse(url_name, kwargs=self.url_kwargs)

    def __str__(self):
        return self.name


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
