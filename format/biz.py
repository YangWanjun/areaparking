import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.template.context_processors import csrf

from . import models
from contract.models import Task, Subscription
from utils import common, constants
from utils.app_base import get_total_context


def get_subscription_confirm_html(request, subscription, **kwargs):
    """申込確認書のHTMLを取得する。

    :param request:
    :param kwargs:
    :return:
    """
    report = get_object_or_404(models.ReportSubscriptionConfirm, pk=subscription.subscription_confirm_format_id)
    parking_lot = subscription.parking_lot
    t = Template(report.content)
    ctx = Context(kwargs)
    ctx.update(get_total_context(
        parking_lot=parking_lot,
        subscription=subscription,
    ))
    ctx.update(csrf(request))
    html = t.render(ctx)
    title = '{0}_{1}'.format(parking_lot.name, constants.REPORT_SUBSCRIPTION_CONFIRM)
    return title, html


def get_subscription_html(request, subscription, **kwargs):
    """申込書のHTMLを取得する。

    :param request:
    :param kwargs:
    :return:
    """
    report = get_object_or_404(models.ReportSubscription, pk=subscription.subscription_format_id)
    parking_lot = subscription.parking_lot
    t = Template(report.content)
    ctx = Context(kwargs)
    ctx.update(get_total_context(
        parking_lot=parking_lot,
        subscription=subscription,
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


def get_user_subscription_steps(signature=None):
    """ユーザー申込みのステップ数

    :return:
    """
    url_kwargs = {'signature': signature}
    step1 = models.Step(step="①", name="申込み基本情報", url_kwargs=url_kwargs)
    step2 = models.Step(step="②", name="申込者分類選択", prev_step=step1, url_kwargs=url_kwargs)
    step3 = models.Step(step="③", name="申込者情報入力", prev_step=step2, url_kwargs=url_kwargs)
    step4 = models.Step(step="④", name="申込み確認", prev_step=step3, url_kwargs=url_kwargs)
    step5 = models.Step(step="⑤", name="申込み完了", prev_step=step4, url_kwargs=url_kwargs)
    step1.next_step = step2
    step2.next_step = step3
    step3.next_step = step4
    step4.next_step = step5
    return [step1.to_json(), step2.to_json(), step3.to_json(), step4.to_json(), step5.to_json()]


def generate_subscription_pdf(request, subscription, **kwargs):
    """ユーザー申込完了時、申込確認書と申込書のPDFを作成する。

    :param request:
    :param subscription:
    :param kwargs:
    :return:
    """
    # 申込確認書のＰＤＦファイルを追加する。
    title, html = get_subscription_confirm_html(request, subscription, **kwargs)
    data = generate_report_pdf_binary(html)
    for report in subscription.reports.filter(name=constants.REPORT_SUBSCRIPTION_CONFIRM):
        report.delete()
    content_file = ContentFile(data.getvalue(), name='subscription.pdf')
    report_file = models.ReportFile(content_object=subscription, name=constants.REPORT_SUBSCRIPTION_CONFIRM,
                                    path=content_file)
    report_file.save()
    # 申込書のＰＤＦファイルを追加する。
    title, html = get_subscription_html(request, subscription, **kwargs)
    data = generate_report_pdf_binary(html)
    for report in subscription.reports.filter(name=constants.REPORT_SUBSCRIPTION):
        report.delete()
    content_file = ContentFile(data.getvalue(), name='subscription.pdf')
    report_file = models.ReportFile(content_object=subscription, name=constants.REPORT_SUBSCRIPTION,
                                    path=content_file)
    report_file.save()
