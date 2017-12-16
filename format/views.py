import urllib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from . import biz
from contract.models import Task
from parkinglot.models import ParkingLot
from utils.django_base import BaseView, BaseTemplateView


# Create your views here.
class UserOperationView(BaseTemplateView):
    template_name = 'format/format_base.html'

    def get_context_data(self, **kwargs):
        context = super(UserOperationView, self).get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs.get('task_id'))
        if task.url_links:
            urls = [url for url in task.url_links.split(',') if url]
            context.update({'urls': urls})
        return context


class SubscriptionConfirmView(BaseView):

    def get(self, request, *args, **kwargs):
        html = biz.get_subscription_confirm_html(**kwargs)
        return HttpResponse(html)


class SubscriptionView(BaseView):

    def get(self, request, *args, **kwargs):
        html = biz.get_subscription_html(**kwargs)
        return HttpResponse(html)


class GenerateSubscriptionConfirmPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
        html = biz.get_subscription_confirm_html(**kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + parking_lot.name
        return response


class GenerateSubscriptionPdfView(BaseView):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
        html = biz.get_subscription_html(**kwargs)
        data = biz.generate_report_pdf_binary(html)
        response = HttpResponse(data, content_type="application/pdf")
        response['Content-Disposition'] = "filename=" + parking_lot.name
        return response
