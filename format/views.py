from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, Template

from . import models
from parkinglot.models import ParkingLot
from contract.models import TempContractor, Task
from utils.app_base import get_total_context
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
        report = get_object_or_404(models.ReportSubscriptionConfirm, pk=kwargs.get('report_id'))
        parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
        contractor = get_object_or_404(TempContractor, pk=kwargs.get('contractor_id'))
        t = Template(report.content)
        ctx = Context(kwargs)
        ctx.update(get_total_context(
            parking_lot=parking_lot,
            contractor=contractor,
        ))
        html = t.render(ctx)
        return HttpResponse(html)
