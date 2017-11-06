# -*- coding: utf8 -*-
from __future__ import unicode_literals
import datetime

from django import forms
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.db import models
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.utils.decorators import method_decorator


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

    # def delete(self, using=None, keep_parents=False):
    #     self.is_deleted = True
    #     self.deleted_date = datetime.datetime.now()
    #     self.save()


class BaseAdmin(admin.ModelAdmin):

    def get_actions(self, request):
        actions = super(BaseAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class BaseAdminChangeOnly(BaseAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseForm(forms.ModelForm):
    pass


@method_decorator(login_required(login_url='/admin/login/?next=/'), name='dispatch')
class BaseView(View, ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        kwargs.update({
            'request': request
        })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass


class BaseTemplateView(TemplateResponseMixin, BaseView):

    def get_template_names(self):
        template_names = super(BaseTemplateView, self).get_template_names()
        return template_names
