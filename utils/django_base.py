import traceback

from django import forms
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.gis.db import models
from django.core.management.base import BaseCommand
# from django.db import models
from django.forms import widgets
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.utils.decorators import method_decorator
from django.utils.html import mark_safe, format_html

from rest_framework import serializers, status, pagination
from rest_framework.compat import set_rollback
from rest_framework.response import Response
from rest_framework.views import exception_handler

from material.frontend.views import ModelViewSet, DetailModelView, ListModelView, UpdateModelView

from utils import errors
from utils.common import Setting


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

    def get_actions(self, request):
        actions = super(BaseAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseAdminReadOnly(BaseAdminChangeOnly):

    class Media:
        js = (
            '/static/js/readonly.js',
        )

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


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


@method_decorator(login_required, name='dispatch')
class BaseView(BaseViewWithoutLogin):
    pass


@method_decorator(login_required, name='dispatch')
class BaseTemplateView(BaseTemplateViewWithoutLogin):
    pass


class BaseListModelView(ListModelView):
    paginate_by = 25

    def format_column(self, item, field_name, value):
        if isinstance(value, bool):
            return format_html('<i class="material-icons">{}</i>'.format(
                'panorama_fish_eye' if value else 'close'
            ))
        else:
            formatted = super(ListModelView, self).format_column(item, field_name, value)
            if field_name in self.get_list_display_links(self.get_list_display()):
                formatted = format_html('<a href="{}">{}</a>', self.get_item_url(item), formatted)
            return formatted

    def get_context_data(self, **kwargs):
        context = super(BaseListModelView, self).get_context_data(**kwargs)
        context.update({
            'debug': True,
        })
        return context


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


class BaseModelViewSet(ModelViewSet):
    list_view_class = BaseListModelView
    detail_view_class = BaseDetailModelView
    update_view_class = BaseUpdateModelView

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseModelSerializer(serializers.ModelSerializer):
    pass


class BaseBatch(BaseCommand):

    BATCH_NAME = ''
    BATCH_TITLE = ''

    def __init__(self, *args, **kwargs):
        super(BaseBatch, self).__init__(*args, **kwargs)
        self.batch = self.get_batch_manager()
        self.logger = self.batch.get_logger()
        if not self.batch.id:
            self.batch.title = self.BATCH_TITLE
            self.batch.save()

    def get_batch_manager(self):
        pass

    def handle(self, *args, **options):
        pass

    def execute(self, *args, **options):
        self.logger.info("============== %s実行開始 ==============" % self.BATCH_TITLE)
        try:
            if self.batch.is_active:
                super(BaseBatch, self).execute(*args, **options)
            else:
                self.logger.error(u"%s が有効になっていません。" % (self.BATCH_TITLE,))
        except Exception as ex:
            self.logger.error(ex)
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info("============== %s実行終了 ==============" % self.BATCH_TITLE)

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            action='store',
            dest='username',
            default='batch'
        )


class BaseApiPagination(pagination.PageNumberPagination):

    def get_page_size(self, request):
        s = Setting()
        return s.page_size if s.page_size else 25


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is None:
        if isinstance(exc, errors.MyBaseException):
            data = {'detail': str(exc)}

            set_rollback()
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return None
    else:
        return response
