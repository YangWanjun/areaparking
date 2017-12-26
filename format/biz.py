import os
import json
from io import BytesIO

from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.template.context_processors import csrf

from . import models
from contract.models import Task
from utils import common, constants
from utils.app_base import get_total_context


def get_subscription_confirm_html(request, **kwargs):
    """申込確認書のHTMLを取得する。

    :param request:
    :param kwargs:
    :return:
    """
    task = get_object_or_404(Task, pk=kwargs.get('task_id'))
    report = get_object_or_404(models.ReportSubscriptionConfirm, pk=kwargs.get('report_id'))
    contract = task.process.content_object
    parking_lot = contract.parking_lot
    t = Template(report.content)
    ctx = Context(kwargs)
    ctx.update(get_total_context(
        parking_lot=parking_lot,
        contractor=contract.contractor,
    ))
    ctx.update(csrf(request))
    html = t.render(ctx)
    title = '{0}_{1}'.format(parking_lot.name, constants.REPORT_SUBSCRIPTION_CONFIRM)
    return title, html


def get_subscription_html(request, **kwargs):
    """申込書のHTMLを取得する。

    :param request:
    :param kwargs:
    :return:
    """
    task = get_object_or_404(Task, pk=kwargs.get('task_id'))
    report = get_object_or_404(models.ReportSubscription, pk=kwargs.get('report_id'))
    contract = task.process.content_object
    parking_lot = contract.parking_lot
    t = Template(report.content)
    ctx = Context(kwargs)
    ctx.update(get_total_context(
        parking_lot=parking_lot,
        contractor=contract.contractor,
    ))
    ctx.update(csrf(request))
    html = t.render(ctx)
    title = '{0}_{1}'.format(parking_lot.name, constants.REPORT_SUBSCRIPTION_CONFIRM)
    return title, html


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


def get_user_subscription_steps():
    """ユーザー申込みのステップ数

    :return:
    """
    step1 = models.Step(step="①", name="申込み基本情報")
    step2 = models.Step(step="②", name="申込者分類選択", prev_step=step1)
    step3 = models.Step(step="③", name="申込者情報入力", prev_step=step2)
    step4 = models.Step(step="④", name="申込み確認", prev_step=step3)
    step5 = models.Step(step="⑤", name="申込み完了", prev_step=step4)
    step1.next_step = step2
    step2.next_step = step3
    step3.next_step = step4
    step4.next_step = step5
    return [step1.to_json(), step2.to_json(), step3.to_json(), step4.to_json(), step5.to_json(),]
