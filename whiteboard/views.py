import sys
import json
import operator

from functools import reduce

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse

from . import models, forms
from contract.forms import SubscriptionForm
from utils import errors
from utils.django_base import BaseTemplateView, BaseView, BaseViewWithoutLogin, BaseModelViewSet, BaseListModelView, \
    BaseDetailModelView
from master.models import Config, PushNotification


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('whiteboard:whiteboard_list')


class WhiteBoardListView(BaseListModelView):
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
        q = self.request.GET.get('datatable-search[value]', None)
        if q:
            orm_lookups = ['name__icontains', 'address__icontains',
                           'staff__first_name__icontains', 'staff__last_name__icontains']
            for bit in q.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset

    def get_datatable_config(self):
        config = super(WhiteBoardListView, self).get_datatable_config()
        config['searching'] = True
        return config


class WhiteBoardDetailView(BaseDetailModelView):
    template_name = 'whiteboard/whiteboard_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardDetailView, self).get_context_data(**kwargs)
        context.update({
            'change_url': reverse('admin:parkinglot_parkinglot_change', args=(self.object.pk,)) + '?_popup=1',
        })
        return context


class WhiteBoardViewSet(BaseModelViewSet):
    model = models.WhiteBoard
    list_display = (
        'code', 'name', 'staff', 'category', 'address', 'is_empty', 'position_count',
        'waiting_count', 'is_existed_contractor_allowed', 'is_new_contractor_allowed',
        'free_end_date', 'operation',
    )
    list_display_links = ('id', 'name')
    list_view_class = WhiteBoardListView
    detail_view_class = WhiteBoardDetailView

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class WhiteBoardPositionDetailView(BaseTemplateView):
    template_name = './whiteboard/whiteboard_position_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardPositionDetailView, self).get_context_data(**kwargs)
        whiteboard_position = get_object_or_404(models.WhiteBoardPosition, pk=kwargs.get('pk'))
        subscription_form = SubscriptionForm(initial={
            'parking_lot_id': whiteboard_position.parking_position.parking_lot.pk,
            'parking_position_id': whiteboard_position.parking_position.pk,
        })
        context.update({
            'whiteboard_position': whiteboard_position,
            'subscription_form': subscription_form,
        })
        return context


class WaitingListView(BaseListModelView):

    def get_queryset(self, *args, **kwargs):
        queryset = super(WaitingListView, self).get_queryset()
        q = self.request.GET.get('datatable-search[value]', None)
        if q:
            orm_lookups = ['parking_lot_name__icontains', 'user_name__icontains', 'tel', 'phone']
            for bit in q.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset

    def get_datatable_config(self):
        config = super(WaitingListView, self).get_datatable_config()
        config['searching'] = True
        return config


class WaitingDetailView(BaseDetailModelView):

    def get_context_data(self, **kwargs):
        context = super(WaitingDetailView, self).get_context_data(**kwargs)
        waiting_contact_form = forms.WaitingContactForm(initial={
            'waiting': self.object,
            'contact_user': self.request.user,
        })
        context.update({
            'waiting_contact_form': waiting_contact_form,
        })
        return context


class WaitingViewSet(BaseModelViewSet):
    model = models.Waiting
    list_display = ('user_name', 'parking_lot_name', 'tel', 'phone', 'address1', 'email', 'created_date')
    list_view_class = WaitingListView
    detail_view_class = WaitingDetailView

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class WhiteBoardMapView(BaseTemplateView):
    template_name = './whiteboard/whiteboard_map.html'

    def get_context_data(self, **kwargs):
        context = super(WhiteBoardMapView, self).get_context_data(**kwargs)
        context.update({
            'circle_radius': Config.get_circle_radius(),
        })
        return context


class InquiryViewSet(BaseModelViewSet):
    model = models.Inquiry
    list_display = ('user_name', 'get_gender_display', 'tel', 'parking_lot_name', 'area_name', 'created_date')

    def get_gender_display(self, obj):
        return obj.get_gender_display()

    get_gender_display.short_description = '性別'

    def has_add_permission(self, request):
        return True


class HandbillDistributionView(BaseTemplateView):
    template_name = 'whiteboard/handbilldistribution_list.html'


class HandbillCompanyViewSet(BaseModelViewSet):
    model = models.HandbillCompany
    list_display = ('name', 'unit_price', 'distribute_count')

    def has_add_permission(self, request):
        return True


class TroubleListView(BaseTemplateView):
    template_name = 'whiteboard/trouble_list.html'


class TroubleDetailView(BaseTemplateView):
    template_name = 'whiteboard/trouble_detail.html'


class TroubleAddView(BaseTemplateView):
    template_name = 'whiteboard/trouble_add.html'


class ConstructionListView(BaseTemplateView):
    template_name = 'whiteboard/construction_list.html'


class ConstructionDetailView(BaseTemplateView):
    template_name = 'whiteboard/construction_detail.html'


class ConstructionAddView(BaseTemplateView):
    template_name = 'whiteboard/construction_add.html'


class UpdateSubscription(BaseView):

    def post(self, request, *args, **kwargs):
        result = {}
        subscription = request.POST.get('subscription', None)
        if subscription:
            subscription = json.loads(subscription)
            endpoint = subscription.get('endpoint')
            registration_id = endpoint.split('/')[-1]
            if PushNotification.objects.filter(registration_id=registration_id).count() == 0:
                notification = PushNotification(
                    user=request.user,
                    registration_id=registration_id,
                    key_auth=subscription.get('keys').get('auth'),
                    key_p256dh=subscription.get('keys').get('p256dh')
                )
                notification.save()
            result['error'] = 0
        else:
            result['error'] = 1
        return JsonResponse(result)


class GetNotificationData(BaseViewWithoutLogin):

    def get(self, request, *args, **kwargs):
        registration_id = request.GET.get('registration_id', None)
        data = {}
        if registration_id:
            try:
                notification = PushNotification.objects.get(registration_id=registration_id)
                title = notification.title
                message = notification.message
                url = notification.url
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                title = ''
                message = ''
                url = ''
            data = {
                'title': title,
                'message': message,
                'url': url,
            }
        else:
            data['error'] = 1
        return JsonResponse(data)


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
