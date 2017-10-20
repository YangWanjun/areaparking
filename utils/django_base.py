# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models


class PublicManager(models.Manager):

    # use_for_related_fields = True

    def __init__(self, *args, **kwargs):
        super(PublicManager, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(is_deleted=False)

    def public_all(self):
        return self.get_queryset().filter(*self.args, **self.kwargs)

    def public_filter(self, *args, **kwargs):
        return self.public_all().filter(*args, **kwargs)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u"作成日時")
    updated_date = models.DateTimeField(auto_now=True, editable=False, verbose_name=u"更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()
