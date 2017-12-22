import sys

from django.shortcuts import get_object_or_404, redirect, render, reverse

from material.frontend.views.viewset import ModelViewSet, ListModelView, DetailModelView

from contract.forms import ContractorForm
from utils import errors
from utils.django_base import BaseTemplateView, BaseView
from master.models import Config
from . import models


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('whiteboard:whiteboard_list')


class WhiteBoardListView(ListModelView):
    # paginate_by = 25

    def get_headers_data(self):
        """Readable column titles."""
        for field_name in self.get_list_display():
            attr = self.get_data_attr(field_name)
            if field_name == 'free_end_date':
                label = 'フリー'
            else:
                label = attr.label
            yield field_name, label

    def get_queryset(self, *args, **kwargs):
        queryset = super(WhiteBoardListView, self).get_queryset()
        # q = self.request.POST.get('datatable-search[value]', None)
        # if q:
        #     orm_lookups = ['bk_no__icontains', 'bk_name__icontains', 'address__icontains', 'tanto_name__icontains']
        #     for bit in q.split():
        #         or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
        #         queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset

    # def dispatch(self, request, *args, **kwargs):
    #     """Handle for browser HTTP and AJAX requests from datatables."""
    #     if not self.has_view_permission(self.request):
    #         raise PermissionDenied
    #     self.request_form = DatatableRequestForm(request.POST, prefix='datatable')
    #     self.object_list = self.get_object_list()
    #     if 'HTTP_DATATABLE' in request.META:
    #         handler = self.get_json_data
    #     elif request.method.lower() in self.http_method_names:
    #         handler = getattr(
    #             self, request.method.lower(), self.http_method_not_allowed)
    #     else:
    #         handler = self.http_method_not_allowed
    #     return handler(request, *args, **kwargs)

    # def get_datatable_config(self):
    #     config = super(WhiteBoardListView, self).get_datatable_config()
    #     config['sServerMethod'] = 'POST'
    #     headers = {'X-CSRFToken': get_token(self.request)}
    #     config['ajax'].update({
    #         'headers': headers,
    #     })
    #     return config


class WhiteBoardDetailView(DetailModelView):
    template_name = 'whiteboard/whiteboard_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardDetailView, self).get_context_data(**kwargs)
        context.update({
            'change_url': reverse('admin:parkinglot_parkinglot_change', args=(self.object.pk,)) + '?_popup=1',
        })
        return context


class WhiteBoardViewSet(ModelViewSet):
    model = models.WhiteBoard
    list_display = (
        'code', 'name', 'staff', 'category', 'address', 'is_empty', 'position_count', 'contract_count',
        'temp_contract_count', 'waiting_count', 'is_existed_contractor_allowed', 'is_new_contractor_allowed',
        'free_end_date',
    )
    list_display_links = ('id', 'name')
    list_view_class = WhiteBoardListView
    detail_view_class = WhiteBoardDetailView

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class WhiteBoardPositionDetailView(BaseTemplateView):
    template_name = './whiteboard/parking_position_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardPositionDetailView, self).get_context_data(**kwargs)
        whiteboard_position = get_object_or_404(models.WhiteBoardPosition, pk=kwargs.get('pk'))
        contractor_form = ContractorForm()
        context.update({
            'whiteboard_position': whiteboard_position,
            'temp_contractor_form': contractor_form,
        })
        return context


# class WaitingListView(ListModelView):
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = super(WaitingListView, self).get_queryset()
#         q = self.request.GET.get('datatable-search[value]', None)
#         if q:
#             orm_lookups = ['parking_lot__buken__bk_name__icontains', 'name__icontains', 'address1__icontains', 'address2__icontains']
#             for bit in q.split():
#                 or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
#                 queryset = queryset.filter(reduce(operator.or_, or_queries))
#         return queryset
#
#     def get_datatable_config(self):
#         config = super(WaitingListView, self).get_datatable_config()
#         config['searching'] = True
#         return config
#
#     def get_context_data(self, **kwargs):
#         context = super(WaitingListView, self).get_context_data(**kwargs)
#         context.update({
#             'has_filter': True,
#         })
#         return context
#
#
# class WaitingCreateView(CreateModelView):
#     form_class = forms.WaitingAddForm
#
#     def get_initial(self):
#         initials = super(WaitingCreateView, self).get_initial()
#         parking_lot_id = self.request.GET.get('parking_lot_id', None)
#         if parking_lot_id:
#             parking_lot = get_object_or_404(parkinglot_model.ParkingLot, pk=parking_lot_id)
#             initials.update({
#                 'parking_lot': parking_lot
#             })
#         return initials
#
#
# class WaitingUpdateView(UpdateModelView):
#     form_class = forms.WaitingForm
#
#     def report(self, message, level=messages.INFO, fail_silently=True, **kwargs):
#         """Construct message and notify the user."""
#         opts = self.model._meta
#
#         url = reverse('{}:{}_detail'.format(
#             opts.app_label, opts.model_name), args=[self.object.pk])
#         link = format_html(u'<a href="{}">{}</a>', urlquote(url), force_text(self.object))
#         name = force_text(opts.verbose_name)
#
#         options = {
#             'link': link,
#             'name': name
#         }
#         options.update(kwargs)
#         message = format_html(_(message).format(**options))
#         messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)
#
#
# class WaitingListViewSet(ModelViewSet):
#     model = models.Waiting
#     list_display = ('parking_lot', 'name', 'tel1', 'address1', 'email', 'created_date')
#     list_display_links = ('parking_lot', 'name')
#     update_view_class = WaitingUpdateView
#     list_view_class = WaitingListView
#     create_view_class = WaitingCreateView


class WhiteBoardMapView(BaseTemplateView):
    template_name = './whiteboard/whiteboard_map.html'

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardMapView, self).get_context_data(**kwargs)
        context.update({
            'circle_radius': Config.get_circle_radius(),
        })
        return context


def handler500(request):
    print('500 ERROR!!!')
    cls, exception, traceback = sys.exc_info()
    context = {
        'request_path': request.path,
    }
    if isinstance(exception, errors.SettingException):
        template = 'error_500.html'
    else:
        template = '500.html'
    return render(request, template, context, status=500)
