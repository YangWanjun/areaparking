import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, Template

from . import models, biz
from parkinglot.models import ParkingLot
from contract.models import TempContractor
from utils.django_base import BaseView


# Create your views here.
class SubscriptionView(BaseView):

    def get(self, request, *args, **kwargs):
        report = get_object_or_404(models.ReportSubscription, pk=kwargs.get('report_id'))
        parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
        contractor = get_object_or_404(TempContractor, pk=kwargs.get('contractor_id'))
        t = Template(report.content)
        ctx = Context(kwargs)
        company_info = biz.get_company_context()
        lot_info = biz.get_parking_lot_context(parking_lot)
        contractor_info = biz.get_contractor_context(contractor)
        ctx.update(company_info)
        ctx.update(lot_info)
        ctx.update(contractor_info)
        ctx.update({
            'current_date': datetime.date.today(),
        })
        html = t.render(ctx)
        return HttpResponse(html)
