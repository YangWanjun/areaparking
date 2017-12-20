# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import re
import logging
import pdfkit
import datetime
import random
import math

from calendar import monthrange

from django.conf import settings


def get_root_path():
    """アプリのルートパスを取得する

    :return:
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_path():
    """インポートするデータのパスを取得する。

    :return:
    """
    return os.path.join(get_root_path(), 'data')


def get_temp_path():
    """一時フォルダーを取得する。

    :return:
    """
    path = os.path.join(settings.MEDIA_ROOT, 'temp')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_user_subscription_path():
    path = os.path.join(settings.MEDIA_ROOT, 'user_subscription')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_temp_file(ext):
    """指定拡張子の一時ファイルを取得する。

    :param ext:
    :return:
    """
    temp_root = get_temp_path()
    file_name = "{0}_{1}.{2}".format(
        datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),
        random.randint(10000, 99999),
        ext
    )
    temp_file = os.path.join(temp_root, file_name)
    return temp_file


def get_num_from_str(value):
    try:
        return int(re.sub(r'[^\d]*', '', value))
    except ValueError:
        return 0


def get_batch_logger():
    return logging.getLogger('revolution.management.commands')


def get_ap_logger():
    """営業システムのロガーを取得する。

    :return:
    """
    return logging.getLogger('area_parking')


def generate_pdf_from_string(html, out_path):
    logger = get_ap_logger()
    try:
        # config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        # TODO: パスに日本語があったら、エラーになる。暫定対策：英語にしてから、また日本語名に変更する。
        options = {
            'encoding': "UTF-8",
            'page-size': 'A4',
            'dpi': 300,
        }
        # css = ['']
        pdfkit.from_string(html, out_path, options=options)
    except Exception as ex:
        logger.error(str(ex))


def get_parking_lot_image_path(self, filename):
    """駐車場に関する写真の格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    prefix = 'images/'
    name = '{}_{}'.format(self.parking_lot.name, datetime.datetime.now().strftime('%y%m%d%H%M%S%f'))
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_parking_lot_doc_path(self, filename):
    """駐車場に関する書類の格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    prefix = 'docs/{}/'.format(self.parking_lot.name)
    return prefix + filename


def get_report_path(self, filename):
    """帳票の格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    new_name = filename
    prefix = ''
    content_object = self.content_object
    if content_object.__class__.__name__ == 'Task':
        prefix = 'user_subscription/'
        parking_lot = content_object.process.content_object.parking_lot
        contractor = content_object.process.content_object.contractor
        ext = os.path.splitext(filename)[1]
        new_name = "{0}_{1}_{2}{3}".format(
            parking_lot.name,
            contractor.name,
            datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),
            ext
        )
    return prefix + new_name


def get_report_format(self, filename):
    """各帳票フォーマットの格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    prefix = 'reports/{}/'.format(self.parking_lot.name)
    return prefix + filename


def get_days_by_month(date):
    """指定日付の月の日数を取得する。

    :param date:
    :return:
    """
    month, days = monthrange(date.year, date.month)
    return days


def get_integer(value, decimal_type):
    """小数がある場あるの処理方法

    :param value:
    :param decimal_type:
    :return:
    """
    if value:
        if decimal_type == '0':
            # 切り捨て
            return math.floor(value)
        elif decimal_type == '1':
            # 四捨五入
            return round(value)
        elif decimal_type == '2':
            # 切り上げ
            return math.ceil(value)
    else:
        return 0
