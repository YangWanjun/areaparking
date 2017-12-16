import os
from io import BytesIO

from django.shortcuts import get_object_or_404
from django.template import Context, Template

from . import models
from parkinglot.models import ParkingLot
from contract.models import TempContractor
from utils import common
from utils.app_base import get_total_context


def get_subscription_confirm_html(**kwargs):
    """申込確認書のHTMLを取得する。

    :param kwargs:
    :return:
    """
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
    return html


def get_subscription_html(**kwargs):
    """申込書のHTMLを取得する。

    :param kwargs:
    :return:
    """
    report = get_object_or_404(models.ReportSubscription, pk=kwargs.get('report_id'))
    parking_lot = get_object_or_404(ParkingLot, pk=kwargs.get('lot_id'))
    contractor = get_object_or_404(TempContractor, pk=kwargs.get('contractor_id'))
    t = Template(report.content)
    ctx = Context(kwargs)
    ctx.update(get_total_context(
        parking_lot=parking_lot,
        contractor=contractor,
    ))
    html = t.render(ctx)
    return html


def generate_report_pdf_binary(html):
    temp_file = common.get_temp_file('pdf')
    try:
        common.generate_pdf_from_string(html, temp_file)
        data = open(temp_file, 'rb').read()
        return BytesIO(data)
    except Exception as ex:
        logger = common.get_ap_logger()
        logger.error(ex)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
