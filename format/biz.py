import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.template.context_processors import csrf

from . import models
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


def create_steps(steps, url_pattern=None, url_kwargs=None):
    """

    :param steps:
    :param url_pattern:
    :param url_kwargs:
    :return:
    """
    prev_step = None
    step_list = []
    for i, code_name in enumerate(steps):
        code, name = code_name
        step = models.Step(step=code, name=name, prev_step=prev_step, url_pattern=url_pattern, url_kwargs=url_kwargs)
        if prev_step:
            prev_step.next_step = step

        prev_step = step
        step_list.append(step)

    return step_list


def get_user_subscription_simple_steps(signature=None):
    """申込み用フォーム(車室の一時確保に必要な項目)のステップ数

    :param signature:
    :return:
    """
    url_pattern = 'format:user_subscription_simple_step%s'
    url_kwargs = {'signature': signature}
    step_list = create_steps(
        [
            ('①', '申込み基本情報'),
            ('②', '申込み完了'),
        ],
        url_pattern=url_pattern,
        url_kwargs=url_kwargs,
    )
    return [step.to_json() for step in step_list]


def get_user_subscription_steps(signature=None):
    """ユーザー申込みのステップ数

    :return:
    """
    url_pattern = 'format:user_subscription_step%s'
    url_kwargs = {'signature': signature}
    step_list = create_steps(
        [
            ('①', '申込み基本情報'),
            ('②', '申込者分類選択'),
            ('③', '申込者情報入力'),
            ('④', '申込み確認'),
            ('⑤', '申込み完了'),
        ],
        url_pattern=url_pattern,
        url_kwargs=url_kwargs,
    )
    return [step.to_json() for step in step_list]


def get_user_contract_steps(signature=None):
    """ユーザー契約のステップ数

    :return:
    """
    url_pattern = 'format:user_contract_step%s'
    url_kwargs = {'signature': signature}
    step_list = create_steps(
        [
            ('①', '送付状'),
            ('②', '契約金計算書'),
            ('③', '駐車場利用契約書'),
            ('④', '契約完了'),
        ],
        url_pattern=url_pattern,
        url_kwargs=url_kwargs,
    )
    return [step.to_json() for step in step_list]


def get_contract_cancellation_steps(signature=None):
    """ユーザー契約のステップ数

    :return:
    """
    url_pattern = 'format:user_contract_cancellation_step%s'
    url_kwargs = {'signature': signature}
    step_list = create_steps(
        [
            ('①', '退出届'),
            ('②', '退出届送付完了'),
        ],
        url_pattern=url_pattern,
        url_kwargs=url_kwargs,
    )
    return [step.to_json() for step in step_list]


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
