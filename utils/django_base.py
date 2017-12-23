# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db import models
from django.forms import widgets
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.utils.decorators import method_decorator
from django.utils.html import mark_safe

from material.frontend.views import ModelViewSet, DetailModelView, ListModelView, UpdateModelView


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


class BaseViewModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pass

    def delete(self, using=None, keep_parents=False):
        pass


class BaseAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/bundle.js',
        )

    def get_actions(self, request):
        actions = super(BaseAdmin, self).get_actions(request)
        # if 'delete_selected' in actions:
        #     del actions['delete_selected']
        return actions

    def response_change(self, request, obj):
        if request.GET.get('_popup', None) == '1':
            return HttpResponse('''
               <script type="text/javascript">
                  window.opener.location.reload();
                  window.close();
               </script>''')
        else:
            response = super(BaseAdmin, self).response_change(request, obj)
            return response


class BaseAdminEditor(BaseAdmin):
    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/tinymce.init.js',
        )


class BaseAdminChangeOnly(BaseAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseForm(forms.ModelForm):
    pass


class DynamicListWidget(widgets.Widget):
    input_type = 'text'
    template_name = 'django/forms/widgets/text.html'

    def get_context(self, name, value, attrs):
        context = super(DynamicListWidget, self).get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context

    def render(self, name, value, attrs=None, renderer=None):
        label = ''
        verbose_name = ''
        if isinstance(value, models.Model):
            verbose_name = str(value)
            value = value.pk
        if hasattr(self, 'form_instance'):
            label = self.form_instance.fields[name].label if self.form_instance else ''
            if not verbose_name and self.form_instance.instance and hasattr(self.form_instance.instance, name):
                verbose_name = str(getattr(self.form_instance.instance, name))
        element_id = attrs.get('id')
        text_name = element_id.replace('id_', 'ac_')
        attrs.update({'id': element_id.replace('id_', 'id_ac_')})
        text_html = super(DynamicListWidget, self).render(text_name, verbose_name, attrs, renderer)
        hidden_html = '<input type="hidden" id="{0}" name="{1}" value="{2}" />'.format(
            element_id, element_id.lstrip('id_'), value or ''
        )

        output = list()
        output.append('<div class="row">')
        output.append('<div class="input-field col s12" id="id_{0}_container">'.format(name))
        output.append(hidden_html)
        output.append(text_html)
        html = '<label for="id_ac_{0}" class="">{1}</label>'.format(
            name, label
        )
        output.append(html)
        output.append('</div>')
        output.append('</div>')
        return mark_safe('\n'.join(output))


@method_decorator(login_required, name='dispatch')
class BaseView(View, ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        kwargs.update({
            'request': request,
            'debug': True,
        })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass


class BaseTemplateView(TemplateResponseMixin, BaseView):

    def get_template_names(self):
        template_names = super(BaseTemplateView, self).get_template_names()
        return template_names


class BaseViewWithoutLogin(View, ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BaseViewWithoutLogin, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        kwargs.update({
            'request': request,
            'debug': True,
        })
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass


class BaseTemplateViewWithoutLogin(TemplateResponseMixin, BaseViewWithoutLogin):

    def get_template_names(self):
        template_names = super(BaseTemplateViewWithoutLogin, self).get_template_names()
        return template_names


class BaseModelViewSet(ModelViewSet):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseListModelView(ListModelView):
    pass


class BaseDetailModelView(DetailModelView):

    def get_context_data(self, **kwargs):
        context = super(BaseDetailModelView, self).get_context_data(**kwargs)
        context.update({
            'debug': True,
        })
        return context


class BaseUpdateModelView(UpdateModelView):
    def get_context_data(self, **kwargs):
        context = super(BaseUpdateModelView, self).get_context_data(**kwargs)
        context.update({
            'debug': True,
        })
        return context
